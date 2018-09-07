let log = console.log.bind(console)


let ajax = function (method, path, data, responseCallback) {
    let r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    // 这个不是必须的
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function () {
        if (r.readyState === 4) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            responseData = JSON.parse(r.response)
            log('receive', responseData)
            responseCallback(responseData)
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    log('send', data)
    r.send(data)
}


let apiSendMsgCode = function (form, callback) {
    let path = '/api/send/msg'
    ajax('POST', path, form, callback)
}


let apiArrangeManager = function (user_uuid, form, callback) {
    let path = '/api/manager/arrange/' + user_uuid
    ajax('POST', path, form, callback)
}


function getAllUrlParams(url) {

    // get query string from url (optional) or window
    let queryString = url ? url.split('?')[1] : window.location.search.slice(1)

    // we'll store the parameters here
    let obj = {}

    // if query string exists
    if (queryString) {

        // stuff after # is not part of query string, so get rid of it
        queryString = queryString.split('#')[0]

        // split our query string into its component parts
        let arr = queryString.split('&')

        for (let i = 0; i < arr.length; i++) {
            // separate the keys and the values
            let a = arr[i].split('=')

            // in case params look like: list[]=thing1&list[]=thing2
            let paramNum = undefined
            let paramName = a[0].replace(/\[\d*\]/, function (v) {
                paramNum = v.slice(1, -1)
                return ''
            })

            // set parameter value (use 'true' if empty)
            let paramValue = typeof(a[1]) === 'undefined' ? true : a[1]

            // (optional) keep case consistent
            paramName = paramName.toLowerCase()
            paramValue = paramValue.toLowerCase()

            // if parameter name already exists
            if (obj[paramName]) {
                // convert value to array (if still string)
                if (typeof obj[paramName] === 'string') {
                    obj[paramName] = [obj[paramName]]
                }
                // if no array index number specified...
                if (typeof paramNum === 'undefined') {
                    // put the value on the end of the array
                    obj[paramName].push(paramValue)
                }
                // if array index number specified...
                else {
                    // put the value at that index number
                    obj[paramName][paramNum] = paramValue
                }
            }
            // if param name doesn't exist yet, set it
            else {
                obj[paramName] = paramValue
            }
        }
    }

    return obj
}


// 新增的 api 包裝了 jquery 的常见用法

// 取 form 类型的字段值，比如 val('#id-input-username') -> 'zhangsan'
const val = (selector) => {
    const element = $(selector)
    const v = element.val()
    element.val('')
    return v
}

// 取 一组 同样类型的字段值， 比如取 已选多选框 的 一组值
const val_list = (selector) => {
    return $.map($(selector), (raw_element) => {
        const element = $(raw_element)
        element.attr('checked', false)
        return element.val()
    })
}

// 绑定 点击 事件，比如 click('#id-button-post-add') -> 点击添加 新的 博客
const click = (selector, callback) => $(selector).click(callback)

// 对于从 ajax 取回数据并动态添加到 html 中，事件会丢失，委托可以解决这个问题
const delegated_click = (selector, class_name, callback) => $(selector).delegate(class_name, 'click', callback)

// 发送 表单 并 刷新页面，让新增的数据显示出来。原因是目前 前后端 不完全分离
const post_and_reload = function (path, data) {
    const reload = () => location.reload()
    $.post(path, data).done(reload)
}

const post_json = (path, data, callback) => {
    data = JSON.stringify(data)
    $.ajax(path, {
        method: 'POST',
        contentType: 'application/json',
        data: data,
    }).done((response) => {
        callback(response)
    })
}

const post_json_and_reload = (path, data, callback) => {
    post_json(path, data, response => {
        callback(response)
        location.reload()
    })
}

// 发送 get 请求 并 刷新页面，目前的用途是发送 删除数据的请求
// 通过刷新页面让删除的数据消失在页面上。
// 合理的做法是发送 DELETE 请求，并让前端去特定数据的节点，原因是目前 前后端 不完全分离
const get_and_reload = function (path) {
    const reload = () => location.reload()
    $.get(path).done(reload)
}

const get_with_query = (path, data, callback) => {
    $.ajax(path, {
        method: 'GET',
        data: data,
    }).done(callback)
}

const get_json = (path, callback) => $.get(path).done(callback)

// 一般用在编辑按钮的弹框中，目的是填充之前数据的已有信息
// 用户在此基础上进行修改
const load_one_model = function (path, table) {
    const action = (response) => {
        for (let selector in table) {
            const field = table[selector]
            const value = response[field]
            $(selector).val(value)
        }
    }
    $.get(path).done(action)
}

const load_many_models = (selector, models, template_model) => {
    const container = $(selector)
    container.empty()
    models.forEach((model) => {
        const t = template_model(model)
        container.append(t)
    })
}

// 弹窗用来确定是否删除某个数据
// name 是 数据的名字 callback 是具体执行删除命令的函数
const confirm_of_delete_swal = function (name, callback) {
    const config = {
        title: `确定删除 ${name} 吗？`,
        text: "已删除的信息不能恢复",
        type: "warning",
        confirmButtonClass: "btn-danger",
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        showCancelButton: true,
        closeOnConfirm: false,
        closeOnCancel: false,
    }

    const action = function (is_confirm) {
        if (is_confirm) {
            callback()
            swal("已删除", `${name} 信息删除成功`, "success")
        } else {
            swal("已取消", `${name} 信息删除失败`, "error")
        }
    }

    swal(config, action)
}

const get_current_year = () => {
    const now = new Date()
    return now.getFullYear()
}


const ensure_form_fields_filled = (data, fields) => {
    log('data', data)
    for (let field of fields) {
        if (data[field]) {
            //
        } else {
            swal("表单提交失败", "确保已填写表单的所有必填字段, 必填字段以红色*标注。", "error")
            return false
        }
    }
    return true
}

// 删除确认弹窗函数，无callback
const confirmOfDeleteSwal = (self, name, confirmText) => {
    swal({
            title: `确定删除该${name}吗？`,
            text: `${confirmText}`,
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "确定删除！",
            cancelButtonText: "取消删除！",
            closeOnConfirm: false,
            closeOnCancel: false,

        },
        function (isConfirm) {
            if (isConfirm) {
                window.location = $(self).data('url')
                swal({
                    title: "删除！",
                    text: `该${name}已经被删除`,
                    type: "success",
                    timer: 3600,
                })
            } else {
                swal("取消！", `${name}未删除`, "error")
            }
        })
}