import guilib as ui
import circuitry

component = {
        "textfield": None,
        "textbox": None,
        "circuit": None,
        "resistance": None,
        "capacitance": None,
        "inductance": None,
        "voltage": None,
        "frequency": None,
        "input_form": None,
        "power_form":None,     
        }

state = {
            "r":[],
            "c":[],
            "l":[],          
        }
source = {
            "tot_impedance":[],
            "voltage": 0,
            "frequency": 0,
            "loop_qty": 0,
            }

component_index=("r","c","l")


def open_file():
    """
    Reads a float value from an input field and sets it as the circuit's voltage.
    """
    pass

def save_file():
    pass       

def set_voltage():
    """
    Reads a float value from an input field and sets it as the circuit's frequency.
    """
    try:
        voltage = float(ui.read_field(component["voltage"]))
        frequency = float(ui.read_field(component["frequency"]))
    except ValueError:
        ui.open_msg_window("Error Message", "Input wasn't a valid number", error=True)
    else:
        source["voltage"] = voltage
        source["frequency"] = frequency 
        ui.write_to_textbox(component["textbox"], "Voltage {a:.1f} V".format(a=voltage))
        ui.write_to_textbox(component["textbox"], "Frequency {a:.3f} Hz".format(a=frequency))
    ui.clear_field(component["voltage"])
    ui.clear_field(component["frequency"])
    ui.hide_subwindow(component["power_form"])

def set_impedance():
    """
    Reads a float from an input field and adds a resistor with the read value as
    its resistance. The resistor is added to the sole loop in the circuit.
    Updates the circuit diagram.
    """
    try:
        state["r"] = float(ui.read_field(component["resistance"]))
        state["c"] = float(ui.read_field(component["capacitance"]))
        state["l"] = float(ui.read_field(component["inductance"]))
    except ValueError:
        ui.open_msg_window("Error Message", "Input wasn't a valid number", error=True)
    else:
        zero_values = list(state.values()).count(0)#identifies if serial or parallell connection by counting number of zeros entered
        if zero_values == 3:
            ui.open_msg_window("Error Message", "At least one component should be of non-zero value!", error=True)
        elif zero_values == 2: #serial connection = 2 zeros
            for i in component_index:
                if state[i] != 0:
                    source["tot_impedance"].append((i, state[i]))
        else: #paralell connection = 1 or no zeros
            temp =[]
            for i in component_index:
                if state[i] != 0:
                    temp.append((i, state[i]))
            source["tot_impedance"].append(temp) 

    ui.write_to_textbox(component["textbox"], "Resistance {a:.1f} Ohm \nCapacitance {b:.1f} F \nInductance {c:.1f} H \n".format(a=state["r"], b=state["c"], c=state["l"]))    
    circuitry.draw_voltage_source(component["circuit"], source["voltage"], source["frequency"])
    for i in range (source["loop_qty"]+1):
        circuitry.draw_loop(component["circuit"], source["tot_impedance"], 3, 2, last=False)
    circuitry.draw_circuit(component["circuit"])
    ui.clear_field(component["resistance"])
    ui.clear_field(component["capacitance"])
    ui.clear_field(component["inductance"])
    ui.hide_subwindow(component["input_form"])

def set_new_loop():
    source["loop_qty"] =source["loop_qty"] + 1 
    open_add_component_window()   

def open_add_component_window():
    ui.show_subwindow(component["input_form"])
    """
    Creates a subwindow for entering component values (resistors, capacitors, coils)
    """

def open_add_power_window():
    ui.show_subwindow(component["power_form"])
    """
    Creates a subwindow for entering power source values (voltage, frequency)
    """
    
def main():
    """
    Creates a user interface window with input field, four buttons, and a textbox
    on the left side. The right side contains a circuit diagram.
    """
    testwindow = ui.create_window("test window")
    my_testframe1 = ui.create_frame(testwindow, ui.LEFT)
    my_testframe2 = ui.create_frame(testwindow, ui.LEFT)
    my_button1 = ui.create_button(my_testframe1, "set voltage", open_add_power_window)
    my_button2 = ui.create_button(my_testframe1, "add component", open_add_component_window) #calls the subwindow function
    my_button3 = ui.create_button(my_testframe1, "add loop", set_new_loop) 
    my_button4 = ui.create_button(my_testframe1, "open file", open_file)
    my_button5 = ui.create_button(my_testframe1, "save file", save_file)
    my_button6 = ui.create_button(my_testframe1, "quit", ui.quit)
    my_textbox = ui.create_textbox(my_testframe1, 20, 20)
    my_circuit = circuitry.create_circuit(my_testframe2, 600, 600, 10) #create the circuity functions
    component["textbox"] = my_textbox
    component["circuit"] = my_circuit #saves the circuity function in Component library
    

    
    #subwindow for components
    input_form = ui.create_subwindow("Add component")
    component["input_form"] = input_form
    field_frame = ui.create_frame(input_form)
    button_frame = ui.create_frame(input_form)
    label_frame = ui.create_frame(field_frame)
    input_frame = ui.create_frame(field_frame)
    ui.create_label(label_frame, "resistance")
    component["resistance"] = ui.create_textfield(input_frame)
    ui.create_label(label_frame, "capacitance")
    component["capacitance"] = ui.create_textfield(input_frame)
    ui.create_label(label_frame, "inductance")
    component["inductance"] = ui.create_textfield(input_frame)
    ui.create_button(button_frame, "Save", set_impedance)


   #subwindow for power source
    power_form = ui.create_subwindow("Add power source")
    component["power_form"] = power_form
    field_frame = ui.create_frame(power_form)
    button_frame = ui.create_frame(power_form)
    label_frame = ui.create_frame(field_frame)
    input_frame = ui.create_frame(field_frame)
    ui.create_label(label_frame, "voltage")
    component["voltage"] = ui.create_textfield(input_frame)
    ui.create_label(label_frame, "frequency")
    component["frequency"] = ui.create_textfield(input_frame)
    ui.create_button(button_frame, "Save", set_voltage) 
    
    ui.start()
    
if __name__ == "__main__":
    main()
    print(state)
    print(source)