def generate_html(json_data, filename):
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

    finished_html =  """
        <html>
            <body>
                <form>
                <h1>Student Registration Page</h1>
                    {}
                </form>
            </body>
        </html>
    """.format(html)
    
    with open(filename, "w") as final_html:
        final_html.write(finished_html)


def generate_textbox(element):
    """
        TO-DO: Debug "max" when datatype is integer
    """
    datatype = "text"
    maxAttrName = "maxlength"
    maxlength = element["maxlength"]

    if element["datatype"] == "integer":
        datatype = "number"
        maxAttrName = "max" 
        maxlength = "{}".format((10^int(maxlength)) - 1)

    required = ""
    
    if element["required"] == "true":
        required = "required"


    textbox_html  = """
        <label>
            {}
        </label>
        <input  type="{}"
                name="{}"
                style="width: {}em;" 
                {}="{}" 
                {}
        /><br/><br/>
    """.format(element["caption"]
                ,datatype
                ,element["ename"]
                ,element["size"]
                ,maxAttrName
                ,maxlength
                ,required)

    return textbox_html

def generate_checkbox(element):

    checkbox_html = """ <label>{}</label><br/><br/>""".format(element["caption"])
    datatype = "checkbox"
    for groups in element["group"]:
        checked = ""
        if "checked" in groups and groups["checked"] == "checked":
            checked = "checked"

    

        checkbox_html += """
            <input type={} name="{}" value={} {}
            />
            <label>
            {}
            </label><br/><br/>
            """.format(datatype
                    ,element["ename"]
                    ,groups["value"]
                    ,checked
                    ,groups["caption"])
    return checkbox_html

def generate_select(element):
    slabel_html = """ <label>{}</label><br/><br/>""".format(element["caption"])
    select_html = ""
    for groups in element["group"]:
        

        select_html  += """
        <option value="{}">{}</option>
        """.format(groups["value"]
                   ,groups["caption"])

    final_select = """{}<select name="{}">{}</select><br/><br/>""".format(slabel_html,element["ename"],select_html)
    return final_select

def generate_radio(element):
    label_html = """ <label>{}</label>""".format(element["caption"])
    radio_html = ""
    for groups in element["group"]:

        radio_html += """
        <input type="radio" name="{}" value="{}"/>
        <label>{}</label><br/>
        """.format(element["ename"],groups["value"], groups["caption"])
    final_radio = """ {}<br/>{}<br/>""".format(label_html,radio_html)
    return final_radio

def generate_submit_reset(element, input_type):

    submit_html = """ 
    <input type="{}" name="{}" value="{}"/>
    """.format(input_type, element["ename"], element["caption"])
    return submit_html

def generate_multi(element):
    mlabel_html = """ <label>{}</label>""".format(element["caption"])
    multi_html = ""
    for groups in element["group"]:

        multi_html += """
        <option value="{}">{}</option><br/>
        """.format(groups["value"], groups["caption"])
    final_multiselect = """ {}<select name="{}" size= "{}" multiple>{}</select><br/><br/> """.format(mlabel_html,element["ename"],element["size"],multi_html)
    return final_multiselect