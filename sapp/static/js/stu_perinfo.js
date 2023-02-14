$(function () {
    $("#age_text").text(stuAge());
    $("#btnEditStuInfo").click(function () {
        setLabelInfo();
        handelStudentInfo();
    });

    $("#btnUpdateUserPwd").click(function () {
        $(".error-msg").empty();
        $("#stuUpdatePwdInfo")[0].reset();
    })

    $("#btnUserLogout").click(function () {
        location.href = "/login/";
    })

    bindSendEditInfo(); // 编辑学生信息
    bindSendUpdatePwd(); // 发送学生信息
})

function stuAge() {
    let birthDate = $("#age_text").attr("class");
    let birthYear = birthDate.substring(0, 4);
    let nowYear = new Date().getFullYear();
    return nowYear - birthYear;
}

// 处理学生数据
function handelStudentInfo() {
    $(".error-msg").empty();
    $("#stuPersonInfoForm")[0].reset();
    let fieldName = ["Sno", "Sname", "Ssex", "Birthdate", "AdmissionDate", "Sdept", "Sclass"]
    let formData = []
    $(".stu-info-table tr td:nth-child(2)").each(function () {
        formData.push($(this).text().trim());
    })
    if (formData[2] === '男') {
        formData[2] = 1;
    } else {
        formData[2] = 2;
    }
    formData[3] = $("#age_text").attr("class").replace("年", "-").replace("月", "-").replace("日", "");
    formData[4] = formData[4].replace("年", "-").replace("月", "-").replace("日", "");
    let onlyReadArr = ["", "Sno", "AdmissionDate", "Sdept", "Sclass"];
    for (let i = 0; i < fieldName.length; i++) {
        let inp_id = $("#id_" + fieldName[i]);
        inp_id.val(formData[i]);
        if ($.inArray(fieldName[i], onlyReadArr) > 0) {
            inp_id.attr("readOnly", "readOnly");
        }
    }
    // 时间选择器
    let calend = $("#id_Birthdate");
    calend.datepicker({
        minDate: "-100Y",
        maxDate: new Date(),
        changeMonth: true,
        changeYear: true,
        defaultDate: formData[3]
    });
    calend.datepicker("option", "showAnim", "clip");
    calend.datepicker("option", "dateFormat", "yy-mm-dd");
    $.datepicker.regional['zh-CN'] = {
        prevText: '<上月',
        prevStatus: '显示上月',
        nextText: '下月>',
        nextStatus: '显示下月',
        monthNamesShort: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        dayNamesMin: ['日', '一', '二', '三', '四', '五', '六'],
        dateFormat: 'yy-mm-dd',
    };
    $.datepicker.setDefaults($.datepicker.regional['zh-CN']);
}

// 设置输入框 label
function setLabelInfo() {
    let st = "";
    $(".input-group-text").each(function () {
        if ($(this).text().length < 4) {
            st = "学生" + $(this).text();
            $(this).text(st);
        }
    });
}

// 发送编辑后的学生信息
function bindSendEditInfo() {
    $("#btnSavaStuInfo").click(function () {
        $(".error-msg").empty();
        $.ajax({
            url: "/shome/sinfo/update_info/",
            type: "post",
            data: $("#stuPersonInfoForm").serialize(),
            dataType: "JSON",
            success: function (res) {
                if (res.status) {
                    $("#stuPersonInfoForm")[0].reset();
                    // 关闭表单窗口
                    $("#editPersonInfo").modal("hide");
                    // 刷新页面
                    location.reload();
                    // $("#contentStuBox").load("http://127.0.0.1:8000/shome/sinfo .my-stu-info-box");
                } else {
                    $.each(res.error, function (name, errorList) {
                        console.log("qqqqq");
                        $("#id_" + name).next().text(errorList[0]);
                    })
                }
            }
        })
    })
}


// 发送密码
function bindSendUpdatePwd() {
    $("#btnUpdatePwdSend").click(function () {
        $(".error-msg").empty();
        $.ajax({
            url: "/shome/sinfo/update_pwd/",
            type: "post",
            data: $("#stuUpdatePwdInfo").serialize(),
            dataType: "JSON",
            success: function (res) {
                if (res.status) {
                    $("#stuUpdatePwdInfo")[0].reset();
                    // 关闭表单窗口
                    $("#updatePasswordForm").modal("hide");
                    $("body").append("<div style='position: fixed;top: 50%;left: 50%;transform:translate(-50%,-50%);" +
                        "padding:30px;background-color: rgb(200,245,207);border-radius: 8px'>" +
                        "<h4>提示</h4>" +
                        "<hr>" +
                        "<p style='font-size: 18px'>密码修改成功，2秒后自动跳转至登录页面</p>" +
                        "</div>")
                    setTimeout(function () {
                        location.href = "/login/";
                    }, 2000);
                } else {
                    $.each(res.error, function (name, errorList) {
                        console.log(res.error);
                        $("#id_" + name).next().text(errorList[0]);
                    })
                }
            }
        })
    })
}