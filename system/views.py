from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.http import require_POST, require_GET
from .models import User
from django.http import JsonResponse
from email.header import Header  # 如果包含中文，需要通过Header对象进行编码
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib  # 负责发送邮件
import uuid
from datetime import datetime
from django.utils.timezone import timedelta
from hashlib import md5
import base64


# 跳转至登录和注册页面
def  login_register(request):
    # 判断session中是否还有用户信息
    username = request.session.get('username_session')
    if username:
        return render(request, 'system/index.html')
    return render(request, 'system/login_register.html')

# 验证用户名是否唯一
@require_POST
def unqiue_username(request):
    try:
        # 接收用户名
        username=request.POST.get('username')
        # 查询是否有该用户
        user=User.objects.get(username=username)
        # 有用户返回页面json数据
        return JsonResponse({'code':400,'msg':'用户名已存在,请重新注册!'})
    except User.DoesNotExist as e :
        # 异常信息,表示用户名不存在
        return JsonResponse({'code':200,'msg':'恭喜你,可以注册!'})

# 验证邮箱是否唯一
@require_POST
def unique_email(request):
    try:
        # 接收参数
        email = request.POST.get('email')

        # 查询是否有该用户
        user = User.objects.get(email=email)

        # 有用户返回页面json
        return JsonResponse({'code': 400, 'msg': '邮箱已存在!'})
    except User.DoesNotExist as e:
        # 异常信息说明用户不存在
        return JsonResponse({'code': 200, 'msg': '恭喜你，可以注册!'})


# -----------------email模块构建邮件发送实体对象--------------
# 格式化邮箱(不格式化会被当做垃圾邮件去发送或者发送失败)
def format_addr(s):
    name, addr = parseaddr(s)  # 比如：尚学堂 <java_mail01@163.com>
    # 因为name可能会有中文，需要对中文进行编码
    return formataddr((Header(name, 'utf-8').encode('utf-8'), addr))


# 邮件发送
@require_POST
def send_email(request):

    try:

        # ---------------------准备数据------------------------
        # 发件人邮箱
        from_addr= '18717759247@163.com'
        # 授权码
        password = 'CH1234'
        # 邮件发送的服务地址
        smtp_server = 'smtp.163.com'
        # 接收邮箱
        to_addr = request.POST.get('email')

        # 用户名
        username = request.POST.get('username')
        # 密码
        u_pwd = request.POST.get('password')
        # 使用md5加密
        u_pwd = md5(u_pwd.encode(encoding='utf-8')).hexdigest()
        # 激活码
        code = ''.join(str(uuid.uuid4()).split('-'))
        # 10分钟后的时间戳
        td = timedelta(minutes=10)
        ts = datetime.now() + td
        ts = str(ts.timestamp()).split('.')[0]
        # --------------------------准备数据--------------------------
        print(username, u_pwd, to_addr, code, ts)

        # -----------------------插入数据库数据------------------------
        User.objects.create(username=username, password=u_pwd, email=to_addr, code=code, timestamp=ts)
        # user.save()
        # -----------------------插入数据库数据------------------------

        # ------------------------构建邮件内容对象------------------------
        html = """
                <html>
                    <body>
                        <div>
                        Email 地址验证<br>
                        这封信是由 上海尚学堂 发送的。<br>
                        您收到这封邮件，是由于在 上海尚学堂CRM系统 进行了新用户注册，或用户修改 Email 使用了这个邮箱地址。<br>
                        如果您并没有访问过 上海尚学堂CRM，或没有进行上述操作，请忽略这封邮件。您不需要退订或进行其他进一步的操作。<br>
                        ----------------------------------------------------------------------<br>
                         帐号激活说明<br>
                        ----------------------------------------------------------------------<br>
                        如果您是 上海尚学堂CRM 的新用户，或在修改您的注册 Email 时使用了本地址，我们需要对您的地址有效性进行验证以避免垃圾邮件或地址被滥用。<br>
                        您只需点击下面的链接激活帐号即可：<br>
                        <a href="http://www.crm.com:8000/system/active_accounts/?username={}&code={}&timestamp={}">http://www.crm.com:8000/system/active_accounts/?username={}&amp;code={}&amp;timestamp={}</a><br/>
                        感谢您的访问，祝您生活愉快！<br>
                        此致<br>
                         上海尚学堂 管理团队.
                        </div>
                    </body>
                </html>
             """.format(username, code, ts, username, code, ts)
        msg = MIMEText(html, "html", "utf-8")

        # 标准邮件需要三个头部信息： From To 和 Subject
        # 设置发件人和收件人的信息 u/U:表示unicode字符串
        # 比如：尚学堂 <java_mail01@163.com>
        msg['From'] = format_addr(u'尚学堂<%s>' % from_addr)  # 发件人
        to_name = username  # 收件人名称
        msg['To'] = format_addr(u'{}<%s>'.format(to_name) % to_addr)  # 收件人
        # 设置标题
        # 如果接收端的邮件列表需要显示发送者姓名和发送地址就需要设置Header，同时中文需要encode转码
        msg['Subject'] = Header(u'CRM系统官网帐号激活邮件', 'utf-8').encode()
        # ------------------------构建邮件内容对象-----------end-------------

        # ------------------------------发送--------------start----------------
        # 创建发送邮件服务器的对象
        server = smtplib.SMTP(smtp_server, 25)
        # 设置debug级别0就不打印发送日志，1打印
        server.set_debuglevel(1)
        # 登录发件邮箱
        server.login(from_addr, password)
        # 调用发送方法 第一个参数是发送者邮箱，第二个是接收邮箱，第三个是发送内容
        server.sendmail(from_addr, [to_addr], msg.as_string())
        # 关闭发送
        server.quit()
        # ------------------------------发送----------------end--------------

        # 返回页面提示信息
        return JsonResponse({'code': 200, 'msg': '注册成功，请前往邮箱激活帐号'})
    except smtplib.SMTPException as e:
        print(e)
        # 返回页面提示信息
        return JsonResponse({'code': 400, 'msg': '注册失败，请重新注册'})

# 激活账号
@require_GET
def active_accounts(request):
    try:
        # 获取用户名
        username=request.GET.get('username')
        # 激活码
        code=request.GET.get('code')
        # 过期时间
        ts=request.GET.get('timestamp')
        # 根据用户名和激活码查询是否有该账户
        user=User.objects.get(username=username,code=code,timestamp=ts)
        # 根据过期时间判断该账号是否过期
        now_ts=int(str(datetime.now().timestamp()).split('.')[0])
        if now_ts>int(ts):
            # 链接失效返回提示信息,删除数据库用户信息
            return HttpResponse('<h1>该链接已失效，请重新注册&nbsp;&nbsp;<a href="http://www.crm.com:8000/login_register/">上海尚学堂CRM系统</a></h1>')
        # 没有过期,激活账号,清除激活码,改变状态
        user.code=''# 清除激活码
        user.status=1 #设置为有效账号
        user.save()

        # 返回提示信息
        return  HttpResponse('<h1>帐号激活成功，请前往系统登录&nbsp;&nbsp;<a href="http://www.crm.com:8000/index/">上海尚学堂CRM系统</a></h1>')
    except Exception as e:
        if isinstance( e,User.DoesNotExist):
            return HttpResponse('<h1>该链接已失效，请重新注册&nbsp;&nbsp;<a href="http://www.crm.com:8000/login_register/">上海尚学堂CRM系统</a></h1>')
        return HttpResponse('<h1>不好意思，网络出现了波动，激活失败，请重新尝试</h1>')


# 登录验证
@require_POST
def login_user(request):
    try:
        # 接收参数
        username=request.POST.get('username')
        password=request.POST.get('password')
        remember=request.POST.get('remember')
        remember_5 = request.POST.get('remember_5')

        # 使用md5对密码进行加密
        password_md5=md5(password.encode(encoding='utf-8')).hexdigest()

        # 查询该用户是否存在
        user=User.objects.get(username=username,password=password_md5)

        # 如果用户存在,存储session信息
        request.session['username_session']=username

        # 如果用户存在,前台js存储cookie
        # 存储格式: key ->login_cookie,value->username&password
        # 返回成功提示信息
        context={
            'code':200,
            'msg':'欢迎回来'
        }
        # 如果选择了五天免登录
        if 'true'== remember_5:
            request.session.set_expiry(432000)
        else:
            # 设置session失效时间,关闭浏览器失效
            request.session.set_expiry(0)

        if 'true'== remember:
            context['login_username_cookie']=base64.b64encode(username.encode(encoding='utf-8')).decode(encoding='utf-8')
            context['login_password_cookie'] = base64.b64encode(password.encode(encoding='utf-8')).decode(encoding='utf-8')

        return JsonResponse(context)
    except User.DoesNotExist as e:
        # 返回错误的提示信息
        return JsonResponse({'code':400,'msg':'用户名或密码失效'})


# 跳转至系统首页
def index(request):
    # 判断session中是否还有用户信息
    username=request.session.get('username_session')
    if username:
        return render(request,'system/index.html')

    # 如果不存在,重定向登录页面
    return redirect('system:login_register')


# 提交修改密码表单
# 修改密码
@require_POST
def update_password(request):
    try:
        # 接收参数
        username = request.POST.get('username')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        # 使用md5加密
        old_password_md5 = md5(old_password.encode(encoding='utf-8')).hexdigest()

        # 查询用户密码是否正确
        user = User.objects.get(username=username, password=old_password_md5)

        # 使用md5加密
        new_password_md5 = md5(new_password.encode(encoding='utf-8')).hexdigest()

        # 修改密码
        user.password = new_password_md5
        user.save()

        # 修改密码要重新登录，所以要安全退出
        # 安全退出系统要清除session，所以这里不写

        # 返回页面信息
        return JsonResponse({'code': 200, 'msg': '修改成功'})
    except User.DoesNotExist as e:
        return JsonResponse({'code': 400, 'msg': '原密码输入错误'})


# 安全退出
def logout(request):
    try:
        # 清除session
        request.session.flush()

        # 重定向至登录页面
        return redirect('system:login_register')
    except Exception as e:
        # 重定向至登录页面
        return redirect('system:login_register')



# 点击忘记密直接跳转至修改密码页面
def forget_password(request):
    return render(request,'system/forget_password.html')

# 验证用户名是否唯一
@require_POST
def forget_username(request):
    try:
        # 接收用户名
        username=request.POST.get('username')
        # 查询是否有该用户
        user=User.objects.get(username=username)
        # 有用户返回页面json数据
        return JsonResponse({'code':200,'msg':'用户名存在,请继续输入'})
    except User.DoesNotExist as e :
        # 异常信息,表示用户名不存在
        return JsonResponse({'code':400,'msg':'用户名不存在!'})

# 验证邮箱是否唯一
@require_POST
def forget_email(request):
    try:
        # 接收参数
        email = request.POST.get('email')

        # 查询是否有该用户
        user = User.objects.get(email=email)

        # 有用户返回页面json
        return JsonResponse({'code': 200, 'msg': '邮箱已验证,请继续输入!'})
    except User.DoesNotExist as e:
        # 异常信息说明用户不存在
        return JsonResponse({'code': 400, 'msg': '邮箱不存在!'})


# -----------------email模块构建邮件发送实体对象--------------
# 格式化邮箱(不格式化会被当做垃圾邮件去发送或者发送失败)
def forget_format_addr(s):
    name, addr = parseaddr(s)  # 比如：尚学堂 <java_mail01@163.com>
    # 因为name可能会有中文，需要对中文进行编码
    return formataddr((Header(name, 'utf-8').encode('utf-8'), addr))


# 邮件发送
@require_POST
def forget_send_email(request):

    try:

        # ---------------------准备数据------------------------
        # 发件人邮箱
        from_addr= '18717759247@163.com'
        # 授权码
        password = 'CH1234'
        # 邮件发送的服务地址
        smtp_server = 'smtp.163.com'
        # 接收邮箱
        to_addr = request.POST.get('email')

        # 用户名
        username = request.POST.get('username')


        # 10分钟后的时间戳
        td = timedelta(minutes=10)
        ts = datetime.now() + td
        ts = str(ts.timestamp()).split('.')[0]
        # --------------------------准备数据--------------------------

        # ------------------------构建邮件内容对象------------------------
        html = """
                <html>
                    <body>
                        <div>
                        Email 地址验证<br>
                        这封信是由 上海尚学堂 发送的。<br>
                        您收到这封邮件，是由于在 上海尚学堂CRM系统 进行了新用户注册，或用户修改 Email 使用了这个邮箱地址。<br>
                        如果您并没有访问过 上海尚学堂CRM，或没有进行上述操作，请忽略这封邮件。您不需要退订或进行其他进一步的操作。<br>
                        ----------------------------------------------------------------------<br>
                         帐号激活说明<br>
                        ----------------------------------------------------------------------<br>
                        如果您是 上海尚学堂CRM 的新用户，或在修改您的注册 Email 时使用了本地址，我们需要对您的地址有效性进行验证以避免垃圾邮件或地址被滥用。<br>
                        您只需点击下面的链接激活帐号即可：<br>
                        <a href="http://www.crm.com:8000/system/forget_new_pwd/?username={}&timestamp={}">http://www.crm.com:8000/system/forget_new_pwd/?username={}&amp;timestamp={}</a><br/>
                        感谢您的访问，祝您生活愉快！<br>
                        此致<br>
                         上海尚学堂 管理团队.
                        </div>
                    </body>
                </html>
             """.format(username, ts, username, ts)
        msg = MIMEText(html, "html", "utf-8")

        # 标准邮件需要三个头部信息： From To 和 Subject
        # 设置发件人和收件人的信息 u/U:表示unicode字符串
        # 比如：尚学堂 <java_mail01@163.com>
        msg['From'] = forget_format_addr(u'尚学堂<%s>' % from_addr)  # 发件人
        to_name = username  # 收件人名称
        msg['To'] = forget_format_addr(u'{}<%s>'.format(to_name) % to_addr)  # 收件人
        # 设置标题
        # 如果接收端的邮件列表需要显示发送者姓名和发送地址就需要设置Header，同时中文需要encode转码
        msg['Subject'] = Header(u'CRM系统官网帐号激活邮件', 'utf-8').encode()
        # ------------------------构建邮件内容对象-----------end-------------

        # ------------------------------发送--------------start----------------
        # 创建发送邮件服务器的对象
        server = smtplib.SMTP(smtp_server, 25)
        # 设置debug级别0就不打印发送日志，1打印
        server.set_debuglevel(1)
        # 登录发件邮箱
        server.login(from_addr, password)
        # 调用发送方法 第一个参数是发送者邮箱，第二个是接收邮箱，第三个是发送内容
        server.sendmail(from_addr, [to_addr], msg.as_string())
        # 关闭发送
        server.quit()
        # ------------------------------发送----------------end--------------

        # 返回页面提示信息
        return JsonResponse({'code': 200, 'msg': '邮件发送成功，请前往邮箱确认'})
    except smtplib.SMTPException as e:
        print(e)
        # 返回页面提示信息
        return JsonResponse({'code': 400, 'msg': '发送失败，请重新填写!'})

@require_GET
# 跳转至输入密码页面
def forget_new_pwd(request):
    username=request.GET.get('username')
    ts = request.GET.get('timestamp')


    return render(request,'system/verify_pwd.html',{'username':username,'ts':ts,})

@require_POST
def forget_active_accounts(request):
    try:
        # 获取用户名
        username=request.POST.get('username')
        # 过期时间
        pwd = request.POST.get('password')
        # 过期时间
        ts=request.POST.get('ts')
        # 根据用户名查询是否有该账户
        user=User.objects.get(username=username)
        # 根据过期时间判断该账号是否过期
        now_ts=int(str(datetime.now().timestamp()).split('.')[0])
        if now_ts>int(ts):
            # 链接失效返回提示信息,删除数据库用户信息
            return HttpResponse('<h1>该链接已失效，请重新注册&nbsp;&nbsp;<a href="http://www.crm.com:8000/login_register/">上海尚学堂CRM系统</a></h1>')
        # 没有过期,修改密码,改变状态
        # 使用md5加密
        new_password_md5 = md5(pwd.encode(encoding='utf-8')).hexdigest()

        # 修改密码
        user.password = new_password_md5

        user.save()
        # user.password=pwd ,
        # user.save()

        # 返回页面提示信息
        return JsonResponse({'code': 200, 'msg': '密码修改成功'})
    except smtplib.SMTPException as e:
        print(e)
        # 返回页面提示信息
        return JsonResponse({'code': 400, 'msg': '密码修改失败!'})

