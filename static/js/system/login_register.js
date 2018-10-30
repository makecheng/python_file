//-----------------------------------register start----------------------------//
// 设置页面切换
//首页是注册页面
$('#reg_a').on('click', function () {
    $('#log_b').hide();
    $('#reg_b').show();
});
//点击登录页面 切换到注册页面
$('#log_a').on('click', function () {
    $('#reg_b').hide();
    $('#log_b').show();
});
function check_username() {
    // 失焦事件
    // 获取用户输入的用户名
    var username = $('#reg_name').val();
    var flag = false;
    // 非空判断
    if (undefined == username || '' == username) {
        $('#reg_span').html('用户名不能为空');
        return flag;
    }

    // 验证用户名 字母或者字母加数字必须字母开头 最少4位 最多16位
    var reg = /^[a-zA-Z][a-zA-Z0-9]{4,16}$/

    if (!reg.test(username)) {
        $('#reg_span').html('用户名必须是字母开头，4~16位!');
        return flag;
    }

    // 合法后清空提示
    $('#reg_span').html('');


    // 用户名验证成功后发送ajax请求
    $.ajax({
        'type': 'POST',
        'url': '/system/unique_username/',
        'async': false,
        'data': {
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'username': username
        },
        'dataType': 'json',
        'success': function (result) {
            // 如果是400,返回false
            if (400 == result.code) {
                flag = false;
                $('#reg_span').html(result.msg);
            }
            // 如果是200 正常显示
            if (200 == result.code) {
                flag = true;
                $('#reg_span').html(result.msg);
            }
        },
        'error': function (result) {
            console.log(result);
        }
    });
    return flag;
}
$('#reg_name').on('blur', check_username);
// 验证邮箱格式收否正确
function check_email() {
    // 获取邮箱账号
    var email = $('#reg_email').val();
    var flag = false;

    // 非空判断
    if (undefined == email || '' == email) {
        $('#email_span').html('邮箱不能为空');
        return flag;
    }
    // 判断邮箱格式是否正确
    var reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
    if (!reg.test(email)) {
        $('#email_span').html('请输入正确的邮箱格式');
        return flag;
    }
    // 邮箱格式正确,清空提示信息
    $('#email_span').html('');
    // 邮箱格式正确发送ajax请求
    $.ajax({
        'type': 'POST',
        'url': '/system/unique_email/',
        'async': false,
        'data': {
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'email': email
        },
        'dataType': 'json',
        'success': function (result) {
            // 如果返回是400,设置false返回
            if (400 == result.code) {
                flag = false;
                $('#email_span').html(result.msg);

            }

            // 如果返回是200,正常显示
            if (200 == result.code) {
                flag = true;
                $('#email_span').html(result.msg);
            }
        },
        'error': function (result) {
            console.log(result);

        }
    });
    return flag;
}
$('#reg_email').on('blur', check_email);
// 验证密码,必须是数字大小写字母特殊符号组成,最少8位,最多16位
function check_pwd() {
    // 获取密码
    var pwd = $('#reg_pwd1').val();
    // 判断密码长度是否是8~16位
    if (pwd.length > 16 || pwd.length < 8) {
        $('#pwd_span').html('密码在8~16位!');
        return false;
    }
    // 验证密码
    var reg = /^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[#@*&.])[a-zA-Z\d#@*&.]{8,16}$/;

    if (!reg.test(pwd)) {
        $('#pwd_span').html('请输入正确的密码');
        return false;
    }
    // 密码合法后清空提示
    $('#pwd_span').html("");
    return true
}
$('#reg_pwd1').on('blur', check_pwd);
// 重复密码 获取密码的值进行比较
function check_pwd2() {
    // 获取第一次的密码
    var pwd1 = $('#reg_pwd1').val().trim();
    // 获取第二次输入的密码
    var pwd2 = $('#reg_pwd2').val().trim();
    // 非空判断
    if (undefined == pwd2 || '' == pwd2) {
        $('#pwd_span').html('没有输入重复密码,请重新输入!');
        return false;
    }

    //比较两次输入的密码
    if (pwd1 != pwd2) {
        $('#pwd_span').html('两次输入的密码不一致,请重新输入!');
        return false;
    }
    //密码相同时,清空提示
    $('#pwd_span').html("");
    return true;
}
$('#reg_pwd2').on('blur', check_pwd2);


// 验证密码,必须是数字大小写字母特殊符号组成,最少8位,最多16位
function check_pwd() {
    // 获取密码
    var pwd = $('#reg_pwd1').val();
    // 判断密码长度是否是8~16位
    if (pwd.length > 16 || pwd.length < 8) {
        $('#pwd_span').html('密码在8~16位!');
        return false;
    }
    // 验证密码
    var reg = /^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[#@*&.])[a-zA-Z\d#@*&.]{8,16}$/;

    if (!reg.test(pwd)) {
        $('#pwd_span').html('请输入正确的密码');
        return false;
    }
    // 密码合法后清空提示
    $('#pwd_span').html("");
    return true
}
$('#reg_pwd1').on('blur', check_pwd);
// 重复密码 获取密码的值进行比较
function check_pwd2() {
    // 获取第一次的密码
    var pwd1 = $('#reg_pwd1').val().trim();
    // 获取第二次输入的密码
    var pwd2 = $('#reg_pwd2').val().trim();
    // 非空判断
    if (undefined == pwd2 || '' == pwd2) {
        $('#pwd_span').html('没有输入重复密码,请重新输入!');
        return false;
    }

    //比较两次输入的密码
    if (pwd1 != pwd2) {
        $('#pwd_span').html('两次输入的密码不一致,请重新输入!');
        return false;
    }
    //密码相同时,清空提示
    $('#pwd_span').html("");
    return true;
}
$('#reg_pwd2').on('blur', check_pwd2);


// 点击注册按钮,再次验证数据是否合格
$('#reg_btn').on('click', function () {
    // 点击注册按钮以后,按钮置灰
    $('#reg_btn').attr('disabled', 'true');
    var flag = check_username();
    if (!flag) {
        return;
    }
    var flag = check_email();
    if (!flag) {
        return;
    }
    var flag = check_pwd();
    if (!flag) {
        return;
    }
    var flag = check_pwd2();
    if (!flag) {
        return;
    }



    // 用户信息合法,发送邮件激活账号
    // 获取用户名
    var username = $('#reg_name').val().trim();
    //获取邮箱
    var email = $('#reg_email').val().trim();
    //获取密码
    var pwd = $('#reg_pwd1').val().trim();
    $.ajax({
        'type': 'POST',
        'url': '/system/send_email/',
        'async': false,
        'data': {
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'email': email,
            'username': username,
            'password': pwd
        },
        'dataType': 'json',
        'success': function (result) {
            // 如果是400 设置为false返回
            if (400 == result.code) {
                $('#reg_span').html(result.msg);
            }

            // 如果是200 正常显示
            if (200 == result.code) {
                $('#reg_span').html(result.msg);
            }
        },
        'error': function (result) {
            console.log(result);
        }
    });
});
//---------------------------register end---------------------------------//

//---------------------------login start----------------------------------//
//获取用户名并验证
function login_check_username() {
    // 获取用户名
    username = $('#login_username').val().trim();
    // 对用户名进行非空判断
    if (undefined == username || '' == username) {
        $('#login_span').html('请输入用户名!');
        return false;
    }
    // 清空提示信息
    $('#login_span').html('');
    return true;
}
$('#login_username').on('blur', login_check_username);

// 密码非空验证
function login_check_password() {
    // 获取密码
    password = $('#login_password').val()
    // 对密码进行非空验证
    if (undefined == password || '' == password) {
        $('#login_span').html('请输入密码!');
        return false;
    }
    // 清空提示信息
    $('#login_span').html('');
    return true;
}
$('#login_password').on('blur', login_check_password)


// 登录(验证用户输入的信息是否存在)
function login_user() {
    var flag = login_check_username();
    if (!flag)
        return;
    flag = login_check_password();
    if (!flag)
        return;

    // 判断是否选择记住密码
    var remember = $('#remember').is(':checked');

    // 判断是否选择了五天免密登录
    var remember_5=$('#remember_5').is(':checked');

    // 发送ajax请求验证数据库是否有用户信息
    $.ajax({
        'type': 'POST',
        'url': '/system/login_user/',
        'async': false,
        'data': {
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'username': username,
            'password': password,
            'remember': remember,
            'remember_5':remember_5,
        },
        'dataType': 'json',
        'success': function (result) {
            // 如果是400,显示错误信息
            if (400 == result.code) {
                $('#login_span').html(result.msg)
            }
            // 如果是200,正常显示
            if (200 == result.code) {
                // 如果用户选择记住密码
                if (!(undefined == result.login_username_cookie || null == result.login_username_cookie)) {
                    // 设置cookie 失效15天
                    $.cookie('login_username_cookie', result.login_username_cookie,
                        {'expires': 15, 'path': '/', 'domain': 'crm.com'});
                    $.cookie('login_password_cookie', result.login_password_cookie,
                        {'expires': 15, 'path': '/', 'domain': 'crm.com'});

                }
            }
            window.location.href = '/index/'
        },
        'error': function (result) {
            console.log(result);
        }
    });

}
$("#login_btn").on('click', login_user);


// 进入页面就执行的方法
$(function () {
    // 获取login_cookie,赋值到登录框
    var username = $.cookie('login_username_cookie');
    var password = $.cookie('login_password_cookie');

    // 判断是否存在cookie
    if (!(undefined == username || null == username)) {
        // 使用base64解密
        username = $.base64.decode(username);
        // 赋值到登录框
        $('#login_username').val(username)
    }
    if (!(undefined == password || null == password)) {
        // 使用base64解密
        password = $.base64.decode(password);
        // 赋值到登录框
        $('#login_password').val(password)
    }
});


//---------------------------login end----------------------------------//

//----------------------------forget_password start------------------------//

function forget_username() {
    // 失焦事件
    // 获取用户输入的用户名
    var username = $('#forget_name').val();
    var flag = false;
    // 非空判断
    if (undefined == username || '' == username) {
        $('#forget_span').html('用户名不能为空');
        return flag;
    }

    // 验证用户名 字母或者字母加数字必须字母开头 最少4位 最多16位
    var reg = /^[a-zA-Z][a-zA-Z0-9]{4,16}$/

    if (!reg.test(username)) {
        $('#forget_span').html('用户名必须是字母开头，4~16位!');
        return flag;
    }

    // 合法后清空提示
    $('#forget_span').html('');


    // 用户名验证成功后发送ajax请求
    $.ajax({
        'type': 'POST',
        'url': '/system/forget_username/',
        'async': false,
        'data': {
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'username': username
        },
        'dataType': 'json',
        'success': function (result) {
            // 如果是400,返回false
            if (400 == result.code) {
                flag = false;
                $('#forget_span').html(result.msg);
            }
            // 如果是200 正常显示
            if (200 == result.code) {
                flag = true;
                $('#forget_span').html(result.msg);
            }
        },
        'error': function (result) {
            console.log(result);
        }
    });
    return flag;
}
$('#forget_name').on('blur', forget_username);
// 验证邮箱格式收否正确
function forget_email() {
    // 获取邮箱账号
    var email = $('#forget_email').val();
    var flag = false;

    // 非空判断
    if (undefined == email || '' == email) {
        $('#forget_span').html('邮箱不能为空');
        return flag;
    }
    // 判断邮箱格式是否正确
    var reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
    if (!reg.test(email)) {
        $('#forget_span').html('请输入正确的邮箱格式');
        return flag;
    }
    // 邮箱格式正确,清空提示信息
    $('#forget_span').html('');
    // 邮箱格式正确发送ajax请求
    $.ajax({
        'type': 'POST',
        'url': '/system/forget_email/',
        'async': false,
        'data': {
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'email': email
        },
        'dataType': 'json',
        'success': function (result) {
            // 如果返回是400,设置false返回
            if (400 == result.code) {
                flag = false;
                $('#forget_span').html(result.msg);

            }

            // 如果返回是200,正常显示
            if (200 == result.code) {
                flag = true;
                $('#forget_span').html(result.msg);
            }
        },
        'error': function (result) {
            console.log(result);

        }
    });
    return flag;
}
$('#forget_email').on('blur', forget_email);



// 点击确认按钮,再次验证数据是否合格
$('#reg_btn').on('click', function () {
    // 点击注册按钮以后,按钮置灰
    $('#reg_btn').attr('disabled', 'true');
    var flag = forget_username();
    if (!flag) {
        return;
    }
    var flag = forget_email();
    if (!flag) {
        return;
    }

    // 用户信息合法,发送邮件激活账号
    // 获取用户名
    var username = $('#forget_name').val().trim();
    //获取邮箱
    var email = $('#forget_email').val().trim();

    $.ajax({
        'type': 'POST',
        'url': '/system/forget_send_email/',
        'async': false,
        'data': {
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'email': email,
            'username': username,
        },
        'dataType': 'json',
        'success': function (result) {
            // 如果是400 设置为false返回
            if (400 == result.code) {
                $('#forget_span').html(result.msg);
            }

            // 如果是200 正常显示
            if (200 == result.code) {
                $('#forget_span').html(result.msg);
            }
        },
        'error': function (result) {
            console.log(result);
        }
    });
});



// 点击确认修改后确认
// 点击确认修改后,再次验证数据是否合格
$('#update_pwd_btn').on('click', function () {
    // 点击注册按钮以后,按钮置灰
    var flag = check_pwd();
    if (!flag) {
        return;
    }
    var flag = check_pwd2();
    if (!flag) {
        return;
    }

    // 获取用户名
    var username = $('#forget_username').val();
    //获取时间戳
    var ts = $('#forget_ts').val();
    // 获取密码
    var pwd = $('#reg_pwd1').val();

    $.ajax({
        'type': 'POST',
        'url': '/system/forget_active_accounts/',
        'async': false,
        'data': {
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'username': username,
            'password': pwd,
            'ts':ts,
        },
        'dataType': 'json',
        'success': function (result) {
            // 如果是400 设置为false返回
            if (400 == result.code) {
                $('#pwd_span').html(result.msg);
            }

            // 如果是200 正常显示
            if (200 == result.code) {
                $('#pwd_span').html(result.msg);
            }
        },
        'error': function (result) {
            console.log(result);
        }
    });
});