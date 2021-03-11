def generate_html(json_data):
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
        # elif isEtype and element["etype"] == "multiselectlist":
        #     html += generate_multi(element)
        elif isEtype and element["etype"] == "submit":
            html += generate_submit_reset(element, "submit")
        elif isEtype and element["etype"] == "reset":
            html += generate_submit_reset(element, "reset")

    finished_html =  """
        <html>
            <body>
                <form>
                    {}
                </form>
            </body>
        </html>
    """.format(html)
    print(finished_html)
    # How will you fill the data? Traverse the elements
    # and depending on the etype get the appropriate html string

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
            <input type={} value={} {}
            />
            <label>
            {}
            </label><br/><br/>
            """.format(datatype
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

    final_select = """{}<select>{}</select><br/><br/>""".format(slabel_html,select_html)
    return final_select

def generate_radio(element):
    label_html = """ <label>{}</label>""".format(element["caption"])
    radio_html = ""
    for groups in element["group"]:

        radio_html += """
        <input type="radio" value="{}"/>
        <label>{}</label><br/>
        """.format(groups["value"], groups["caption"])
    final_radio = """ {}<br/>{}<br/>""".format(label_html,radio_html)
    return final_radio

def generate_submit_reset(element, input_type):

    submit_html = """ 
    <input type="{}" value="{}"/>
    """.format(input_type, element["caption"])
    return submit_html