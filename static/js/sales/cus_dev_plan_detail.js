// 初始化编辑器
$('#tt').edatagrid({
    url:'/sales/select_cus_dev_plan_by_sale_chance_id/'+$('#sale_chance_id').val()+'/',
    saveUrl:'/sales/create_cus_dev_plan/'+$('#sale_chance_id').val()+'/',         // 保存时提交URL
    updateUrl:'/sales/update_cus_dev_plan/',       // 修改时提交URL
    destroyUrl:'/sales/delete_cus_dev_plan/',    //删除是提交URL
    pagination:true,  // 显示分页工具栏
    roenumbers:true,   // 显示行号
    width:660,
    height:400,
});

// 添加行
function add() {
    $('#tt').edatagrid('addRow');
}
// 取消行
function cancel() {
    $('#tt').edatagrid('cancelRow');
}
// 删除行
function destroy() {
    $('#tt').edatagrid('destroyRow');
}// 保存行
function save() {
    $('#tt').edatagrid('saveRow');
    setTimeout(function () {
        $('#tt').edatagrid('reload');
    },200);
}
// 开发成功或者开发失败
function update_dev_result(state) {
    $.messager.confirm('系统提示','改操作不可撤销,您确定要继续吗?',function (r) {
        if(r){
            $.get('/sales/update_dev_result/?dev_result='+ state +'&sale_chance_id='+$('#sale_chance_id').val(),function (reault) {
                $.messager.alert('系统提示','操作成功!','info');
                // 隐藏工具栏
                $('#tb').hide()
            });
        }
    });
}





























