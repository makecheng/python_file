from random import randint
from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from customer.models import Customer, LinkMan, Contact, CustomerOrders, OrdersDetail
from system.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.http import require_GET,require_POST
from python_crm.common import Message

# ---------------------------客户信息管理  start--------------------------
@require_GET
# 查询客户名称和客户联系人名称
def select_cname_and_lname_and_uname(request):
    try:

        # 查询客户
        c= Customer.objects.values('id','name').all()

        # 查询联系人
        l =LinkMan.objects.values('id','linkName').all()

        # 查询指派人
        u = User.objects.values('id','username').all()

        # 返回数据
        context={
            'code':200,
            'msg':'success',
            'cs':list(c),
            'ls':list(l),
            'us':list(u)
        }
        return JsonResponse(context)

    except ObjectDoesNotExist as e:
        print(e)
        return JsonResponse({'code':400,'msg':'error'})

# 根据联系人主键查询联系电话
def select_link_phone_by_id(request):
    try:
        # 接收参数
        id = request.GET.get('id')

        # 查询联系电话
        lm =LinkMan.objects.get(pk=id)

        # 返回数据
        return JsonResponse({'code':200,'msg':'sussecc','phone':lm.phone})
    except Exception as e :
        return JsonResponse({'code':400,'msg':'error'})


def customer_index(request):
    '''跳转用户登录首页'''
    return render(request, 'customer/customer.html')

@require_GET
def select_customer_list(request):
    '''查询客户信息列表'''
    try:
        # 获取第几页
        page_num=request.GET.get('page')

        # 获取每页多少条
        page_size=request.GET.get('rows')
        # 查询
        object_list=Customer.objects.values().all().order_by('-id')
        # 接收参数
        name=request.GET.get('name')
        khno=request.GET.get('khno')
        state=request.GET.get('state')

        # 如果有条件则过滤查询
        if name:
            object_list=object_list.filter(name__icontains=name)
        if khno:
            object_list=object_list.filter(khno__icontains=khno)
        if state:
            object_list=object_list.filter(state=state)

        # 初始化分页对象
        p=Paginator(object_list,page_size)
        # 获取指定页数的数据
        data=p.page(page_num).object_list
        # 返回总条数
        count=p.count
        # 返回数据
        context={
            'total':count,
            'rows':list(data)
        }
        return JsonResponse(context)
    except Customer.DoesNotExist as e:
        pass


@csrf_exempt
@require_POST
def create_customer(request):
    '''添加用户信息'''
    try:
        # 接收参数
        data=request.POST.dict()

        # 弹出csrftoken
        data.pop('csrfmiddlewaretoken')
        data.pop('id')
        # 生成客户编号
        result=''
        for i in range(0,3):
            result+=str(randint(0,9))
        khno='KH'+datetime.now().strftime('%Y%m%d%H%M%S')+result
        # 添加信息
        data['khno']=khno
        print(data)
        Customer.objects.create(**data)
        return JsonResponse(Message(msg='添加成功').result())

    except Exception as e:
        pass

@require_GET
def select_customer_by_id(request):
    '''根据主键查询客户信息'''
    try:
        # 接收参数
        id =request.GET.get('id')
        # 查询
        c= Customer.objects.values().filter(pk=id)
        # 返回数据
        return JsonResponse(Message(obj=list(c)).result())
    except Exception as e:
        return JsonResponse(Message(code=400,msg='error').result())

@csrf_exempt
@require_POST
def update_customer(request):
    '''修改客户信息'''
    try:
        # 接收参数
        data=request.POST.dict()
        # 弹出csrftoken
        data.pop('csrfmiddlewaretoken')
        # 弹出主键
        id=data.pop('id')
        # 修改信息
        data['updateDate']=datetime.now()
        Customer.objects.filter(pk=id).update(**data)
        return JsonResponse(Message(msg='修改成功').result())
    except Exception as e:
        pass


@require_GET
def delete_customer(request):
    '''删除客户信息'''
    try:
        # 接收参数
        ids=request.GET.get('ids')
        # 分割字符串
        ids=ids.split(',')
        # 删除
        cs=Customer.objects.filter(pk__in=ids).update(isValid=0)
        return JsonResponse(Message(msg='删除成功').result())
    except Exception as e:
        pass
# ---------------------------客户信息管理  end--------------------------


# ---------------------------客户联系人管理  start--------------------------

@require_GET
def linkman_index(request):
    '''跳转联系人首页'''
    # 接收参数
    id=request.GET.get('id')
    # 查询客户信息
    c= Customer.objects.get(pk=id)
    return render(request,'customer/linkman.html',{'c':c})

@csrf_exempt
@require_POST
def select_linkman_by_customer_id(request,c_id):
    '''根据客户主键查询联系人信息'''
    try:
        # 获取第几页
        page_num = request.POST.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.POST.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        # 查询
        c = Customer.objects.get(pk=c_id)
        object_list = LinkMan.objects.values().filter(customer=c).order_by('-id')

        # 初始化分页对象
        p = Paginator(object_list, page_size)

        # 获取指定页数的数据
        data = p.page(page_num).object_list

        # 返回总条数
        count = p.count

        # 返回数据
        context = {
            'total': count,
            'rows': list(data)
        }
        return JsonResponse(context)
    except LinkMan.DoesNotExist as e:
        pass

@csrf_exempt
@require_POST
def create_linkman(request,c_id):
    '''添加客户联系人'''
    # 接收参数
    data=request.POST.dict()
    # 弹出isNewRecord
    data.pop('isNewRecord')
    # 插入数据
    c=Customer.objects.get(pk=c_id)
    data['customer']=c
    print(data)
    LinkMan.objects.create(**data)
    return JsonResponse(Message(msg='添加成功!').result())

@csrf_exempt
@require_POST
def update_linkman(request):
    '''修改客户联系人'''
    # 接收参数
    data=request.POST.dict()
    # 弹出主键
    id=data.pop('id')
    # 修改参数
    data['updateDate']=datetime.now()
    LinkMan.objects.filter(pk=id).update(**data)
    return JsonResponse(Message(msg='修改成功!').result())

@csrf_exempt
@require_POST
def delete_linkman(request):
    '''删除客户开发计划'''
    # 接收参数
    data=request.POST.dict()
    # 弹出主键
    id=data.pop('id')
    # 逻辑删除
    LinkMan.objects.filter(pk=id).update(isValid=0,updateDate=datetime.now())
    return JsonResponse(Message(msg='删除成功!').result())

#-------------------------------------客户联系人管理---------------------------

# -------------------------------------客户交往记录管理-------------------------
@require_GET
def contact_index(request):
    '''跳转用户交往记录首页'''
    # 接收参数
    id=request.GET.get('id')
    # 查询客户信息
    c=Customer.objects.get(pk=id)
    return render(request,'customer/contact.html',{'c':c})


@csrf_exempt
@require_POST
def select_contact_by_customer_id(request,c_id):
    '''根据客户主键查询客户交往记录信息'''
    try:
        # 获取几页
        page_num=request.POST.get('page',1)
        # 每页多少条
        page_size=request.POST.get('rows',10)
        # 查询
        c=Customer.objects.get(pk=c_id)
        object_list=Contact.objects.values().filter(customer=c).order_by('-id')
        # 初始化分页对象
        p=Paginator(object_list,page_size)
        # 获取指定页数的数据
        data=p.page(page_num).object_list
        # 返回总条数
        count=p.count
        # 返回数据
        context={
            'total':count,
            'rows':list(data)
        }
        return JsonResponse(context)
    except LinkMan.DoesNotExist as e:
        pass

@csrf_exempt
@require_POST
def create_contact(request,c_id):
    '''添加客户交往记录'''
    # 接收参数
    data=request.POST.dict()
    # 弹出isNewRecord
    data.pop('isNewRecord')
    # 插入数据
    c=Customer.objects.get(pk=c_id)
    data['customer']=c
    Contact.objects.create(**data)
    return JsonResponse(Message(msg='添加成功').result())

@csrf_exempt
@require_POST
def update_contact(request):
    '''修改客户交往记录'''
    # 接收参数
    data=request.POST.dict()
    # 弹出主键
    id=data.pop('id')
    # 修改数据
    data['updateDate']=datetime.now()
    Contact.objects.filter(pk=id).update(**data)
    return JsonResponse(Message(msg='修改成功').result())

@csrf_exempt
@require_POST
def delete_contact(request):
    '''删除客户交往记录'''
    # 接收参数
    data=request.POST.dict()
    # 弹出主键
    id=data.pop('id')
    # 删除数据
    Contact.objects.filter(pk=id).update(isValid=0,updateDate=datetime.now())
    return JsonResponse(Message(msg='删除成功!').result())


# -----------------------------客户交往记录管理---------------------------

# ------------------------------客户历史订单管理-------------------------
@require_GET
def order_index(request):
    '''跳转客户历史订单首页'''
    # 接收参数
    id=request.GET.get('id')
    # 查询客户信息
    c=Customer.objects.get(pk=id)
    return render(request,'customer/order.html',{'c':c})


class CustomerOrser(object):
    pass


@csrf_exempt
@require_POST
def select_order_by_customer_id(request,c_id):
    '''根据客户主键查询客户历史订单信息'''
    try:
        # 获取第几页
        page_num=request.POST.get('page',1)
        # 每页多少条
        page_size=request.POST.get('rows',10)
        # 查询
        c=Customer.objects.get(pk=c_id)
        object_list = CustomerOrders.objects.values().filter(customer=c).order_by('-id')
        # 初始化分页对象
        p=Paginator(object_list,page_size)
        # 获取指定页数数据
        data=p.page(page_num).object_list
        # 返回总条数
        count=p.count
        # 返回数据
        context={
            'total':count,
            'rows':list(data)
        }
        return JsonResponse(context)
    except LinkMan.DoesNotExist as e:
        pass

@require_GET
def select_order_by_id(request):
    '''根据订单主键查询订单'''
    try:
        # 接收参数
        order_id=request.GET.get('order_id')
        # 查询
        co=CustomerOrders.objects.values().filter(pk=order_id)
        # 返回信息
        return JsonResponse(Message(obj=list(co)).result())
    except CustomerOrders.DoesNotExist as e :
        pass

@csrf_exempt
@require_POST
def select_order_detail_by_order_id(request,order_id):
    '''根据订单主键查询订单详情'''
    try:
        # 获取第几页
        page_num = request.POST.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.POST.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        # 查询
        # co = CustomerOrders.objects.get(pk=order_id)
        object_list = OrdersDetail.objects.values().filter(order=order_id)

        # 初始化分页对象
        p = Paginator(object_list, page_size)

        # 获取指定页数的数据
        data = p.page(page_num).object_list

        # 返回总条数
        count = p.count

        # 返回数据
        context = {
            'total': count,
            'rows': list(data)
        }
        return JsonResponse(context)
    except OrdersDetail.DoesNotExist as e:
        pass



















