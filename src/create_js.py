def generate_jscript(json_data):
    import_js = """const form = document.getElementById('{}')\n""".format(json_data["name"])
    validations_js = ""
    for element in json_data["elements"]:
        if element.get("etype") == "textbox":
            import_js += generate_imports(element)
            validations_js += generate_validations(element)

    validations_js = get_boilerplate(validations_js)
    final_js = import_js + validations_js + get_helper_functions() + get_sendData_function(json_data["backendURL"])

    with open('./{}.js'.format(json_data["name"]), "w") as f:
        f.write(final_js)

def generate_additional_js(json_data):
    pass

def generate_imports(element):
    import_js = """const {} = document.getElementById('{}')\n""".format(
        element["ename"],element["ename"])
    return import_js

def generate_validations(element):
    validations_js = """
        if({fill}.value === '' || {fill}.value == null){{
            setEmpty(messages, `error_${{{fill}.name}}`)
            messages[`error_${{{fill}.name}}`] += '{fill} is required'
        }}
    """.format(fill=element["ename"])

    condition = """ typeof {}.value != "string" """.format(element["ename"])
    if element["datatype"] == "integer":
        condition = """ !parseInt({}.value) """.format(element["ename"])

    validations_js += """
        if({0}){{
            setEmpty(messages,`error_${{{datamatch}.name}}`)
            messages[`error_${{{datamatch}.name}}`] += '   {datamatch} datatype error'
        }}
    """.format(condition,datamatch=element["ename"])
    return validations_js

def get_boilerplate(validations_js):
    return """
if(form){{
    form.addEventListener('submit', (e) => {{
        let messages = {{}}
        let messages_dup = {{}}
        if(Object.keys(messages_dup).length > 0){{
            for(let error_key of Object.keys(messages_dup)){{
                document.getElementById(error_key).innerText = '';
            }}
        }}
        {}
        if(Object.keys(messages).length > 0){{
            e.preventDefault()      
            for(let error_key of Object.keys(messages)){{
                document.getElementById(error_key).innerText = messages[error_key];
            }}
            messages_dup = messages;
        }}
        else{{
            e.preventDefault()
            submitData()
        }}
    }})
}}
    """.format(validations_js)

def get_helper_functions():
    return """
function setEmpty(messages, msg_key){{
    if(!messages[msg_key]){{
        messages[msg_key] = ""
    }}
}}
    """

def get_sendData_function(url):
    return """
function submitData(){{
    fetch('{}insert', {{
        method: 'POST',
        body: new FormData(form)
    }})
    .then(response => {{
        if(response.status == 200){{
            document.getElementById('webform').innerHTML = '<p>Success</p>'
        }}
        else{{
            document.getElementById('webform').innerHTML = '<p>Error, contact It department</p>'
        }}

    }})
    .catch(error => console.error('Error:', error))
}}
    """.format(url)