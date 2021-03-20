def generate_html(json_data, display=False):
    html = ""
    for element in json_data["elements"]:
        isEtype = "etype" in element
        if isEtype and element["etype"] == "textbox":
            html += generate_textbox(element)
        elif isEtype and element["etype"] == "checkbox":
            html += generate_checkbox(element)
        elif isEtype and element["etype"] == "selectlist":
            html += generate_select(element)
        elif isEtype and element["etype"] == "radiobutton":
            html += generate_radio(element)
        elif isEtype and element["etype"] == "multiselectlist":
            html += generate_multi(element)
        elif isEtype and element["etype"] == "submit":
            html += generate_submit_reset(element, "submit")
        elif isEtype and element["etype"] == "reset":
            html += generate_submit_reset(element, "reset")

    form_id = json_data["name"]
    if display:
        form_id += '_display'
    
    finished_html =  """
<html>
    <head>
        <script defer src="./{}.js"></script>
    </head>
    <body>
        <div id="webform">
            <form id="{}">
                <h1>{}</h1>
                {}
            </form>
        </div>
    </body>
</html>
    """.format(json_data["name"],form_id,json_data["caption"],html)
    
    with open('./{}.html'.format(form_id), "w") as final_html:
        final_html.write(finished_html)


def generate_textbox(element):
    """
        TO-DO: Debug "max" when datatype is integer
    """
    datatype = "text"
    maxlength = element["maxlength"]

    required = ""
    
    if element["required"] == "true":
        required = "required"


    textbox_html  = """
                <label>
                    {}
                </label>
                <input  type="{}"
                        id = "{}"
                        name="{}"
                        size="{}" 
                        maxlength="{}" 
                        {}
                />
                <div id="error_{}"></div><br/><br/>
    """.format(element["caption"]
                ,datatype
                ,element["ename"]
                ,element["ename"]
                ,element["size"]
                ,maxlength
                ,required
                ,element["ename"])

    return textbox_html

def generate_checkbox(element):

    checkbox_html = """ 
                <label>{}</label><br/><br/>""".format(element["caption"])
    datatype = "checkbox"
    for groups in element["group"]:
        checked = ""
        if "checked" in groups and groups["checked"] == "checked":
            checked = "checked"
        checkbox_html += """
                <input type={} name="{}" id="{}" value={} {}/>
                <label>
                {}
                </label><br/><br/>
            """.format(datatype
                    ,element["ename"]
                    ,remove(groups["caption"])
                    ,groups["value"]
                    ,checked
                    ,groups["caption"])
    return checkbox_html

def generate_select(element):
    slabel_html = """<label>{}</label><br/><br/>""".format(element["caption"])
    select_html = ""
    for groups in element["group"]:
        

        select_html  += """<option value="{}">{}</option>""".format(groups["value"]
                   ,groups["caption"])

    final_select = """
                {}
                <select name="{}" id="{}">
                    {}
                </select><br/><br/>""".format(slabel_html,element["ename"],remove(groups["caption"]),select_html)
    return final_select

def generate_radio(element):
    label_html = """<label>{}</label>""".format(element["caption"])
    radio_html = ""
    for groups in element["group"]:

        radio_html += """
                <input type="radio" name="{}" id="{}" value="{}"/>
                <label>{}</label><br/>""".format(element["ename"],groups["caption"],groups["value"], groups["caption"])
    final_radio = """
                {}<br/>
                {}<br/>""".format(label_html,radio_html)
    return final_radio

def generate_submit_reset(element, input_type):

    submit_html = """ 
                <input type="{}" name="{}" id="{}"value="{}"/>
    """.format(input_type, element["ename"], element["caption"], element["caption"])
    return submit_html

def generate_multi(element):
    mlabel_html = """<label>{}</label>""".format(element["caption"])
    multi_html = ""
    for groups in element["group"]:

        multi_html += """
                    <option value="{}">{}</option><br/>
        """.format(groups["value"], groups["caption"])
    final_multiselect = """ 
                {}
                <select name="{}" id="{}" size= "{}" multiple>
                    {}
                </select><br/><br/> """.format(mlabel_html,element["ename"],element["ename"],element["size"],multi_html)
    return final_multiselect

def remove(space):
    return ''.join(e for e in space if e.isalnum())