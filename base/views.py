from django.shortcuts import render
from django.views.decorators.http import require_GET
from base.models import DataDic
from django.http import JsonResponse


@require_GET
def select_customer_level(request):
    '''查询数字字典'''
    try:
        # 接收参数
        dic_name=request.GET.get('dic_name')
        # 查询
        d=DataDic.objects.values('dataDicValue').filter(dataDicName=dic_name).all()
        # 返回数据
        return JsonResponse(list(d),safe=False)
    except Exception as e:
        return JsonResponse({'code':200,'msg':'error'})