# Blocks
There are many different blocks available to control the robot, perform calculations, or display output in the console.

---

## Slots
![Slot Rectangle](static/software_info/images/slot1.png)
Before diving into the block categories, it’s important to understand the concept of **slots**.  
Many blocks contain **gray dashed rectangles** — these represent the **parameters** of a block.  
A slot can accept **variables**, **positions**, or **manual input values**.

![Slot input](static/software_info/images/slot2.png)
If a gray rectangle is visible, you can **drag and drop** a variable into it (typically from the workspace).  
If you **double-click** on the gray rectangle, an **input field** appears where you can enter a value directly.  
To return to the gray slot view, press **right-click** or **Escape**.

However, **not every slot** supports direct value input — some require a variable or position instead.  
For example, in the `Goto position` block, a position variable must be provided.

---

## Movement
Movement blocks are essential for robot motion control.  
Be aware that the robot’s movement is limited to specific coordinate ranges:
- X: 0
- Y: 0
- Z: 0

These maximum axis limits must not be exceeded.

### `Go [] steps on the [x] axis`
![Move Block](static/software_info/images/steps_block.png)
Moves the robot (or motor) along one of the three axes (x, y, or z) by a specified amount.  
The parameter can be a variable or a direct numeric input.  
The axis is selected using the dropdown menu.

### `Goto position: []`
![Goto Block](static/software_info/images/goto_block.png)
Moves the robot to a specific position defined earlier as a **position variable**.  
A quick manual input is not possible here because all three axes (X, Y, Z) must be specified.  
Additionally, standard variables cannot be dropped into this slot — only position variables are accepted.

### `Reset position`
![Reset Block](static/software_info/images/reset_block.png)
Resets the robot to its predefined home position:
- X: -800
- Y: -800
- Z: -30000

The robot will return to these coordinates when this block is executed.

---

## Measurement
![Measure Block](static/software_info/images/measure_block.png)
Currently, there is only one measurement block.  
This block instructs the robot to **start a measurement**.  
Since it takes no parameters, its internal values are predefined in the source code.  
To modify these parameters, you would need to adjust them in the code directly.

---

## Control
### `for [] range [] to []`

![For Block](static/software_info/images/for_block.png)
This code block represents a standard **for loop** (also known as a **counting loop**).  
It allows you to execute a sequence of child blocks a specific number of times.

- The **first slot** represents the **variable** that stores the loop’s counter value.
    This variable increases with each loop iteration, but it must be **manually created and assigned** by the user.
- The **second slot** defines the **starting value** of the loop — the value at which counting begins.
- The **third slot** defines the **end value** — the value **up to (but not including)** which the loop counts.

For example, in the following loop:
![For Block Example](static/software_info/images/for_loop_example.png)

The loop starts at `0` and counts **up to 4**, but **does not include 4**.  
Therefore, the values `0`, `1`, `2`, and `3` will be processed:
![For Block Example Console](static/software_info/images/for_loop_example_console.png)


### `while true`

![While Block](static/software_info/images/while_block.png)
The implemented **while loop** is a **theoretically infinite loop**.  
It continuously repeats its child blocks **an indefinite number of times** until it is explicitly stopped.

The loop can only be **terminated** using a **`Break` block** — for example, in combination with an `If` condition.
This makes it suitable for scenarios where continuous operation is required until a certain condition is met

### `if [] [==] []`
![If Block](static/software_info/images/if_block.png)
A standard **if condition** block.  
It compares the first parameter with the second parameter using the selected comparison operator from the dropdown menu.  
If the condition evaluates to **true**, the child blocks inside are executed; otherwise, the program continues with the next block.

---

## Events
![Break Block](static/software_info/images/break_block.png)
Currently, there is only one event block.  
The **`Break`** block is used to **terminate a loop** (see above).  
It is best used together with an `if` block.  
When executed inside a loop, it immediately stops the loop and continues program execution with the next block.

---

## Constants
![Constants](static/software_info/images/constant_var.png)
This section contains **three predefined variables** that represent the robot’s current position along each axis.  
These values are provided by the robot and server and **cannot be modified** by the user.  
These constants can be used as parameters for other blocks.

---

## Variables
![Variables](static/software_info/images/var_var.png)
By clicking the **`+` button**, you can create a new variable.  
First, you must assign a **name**.  
Certain names and characters are **reserved** and cannot be used.  
Forbidden characters include:  
`"{", "}", "[", "/", "%", "&", "|", " ", "^", "~", "<<", ">>", "==", "<=", ">=", "<", ">", "=", ",", ";", "."`

These restrictions are defined in the program’s code.  
To change them, the source code must be modified.  
Each variable name must be **unique**.

After defining a variable, you can assign it a value in the text field.  
The program only supports **strings** and **integer numbers**.  
Using other data types may cause errors.  
Variables can be deleted using the **gray delete button** next to their entry.

---

## Positions
![Positions](static/software_info/images/positions_var.png)
**Positions** are similar to variables but store **three values** — one for each axis (X, Y, Z).  
This block therefore has three parameters. Variables can also be passed to these parameters. 
This variable type is mainly used by the `Goto position: []` block.

---

## Calculations
![Calculations](static/software_info/images/calc_block.png)
Calculation blocks allow you to assign new values to variables or perform arithmetic operations between them.
- The **first parameter** specifies the target variable whose value should be changed.
- The **second and third parameters** represent the numbers or variables used in the calculation.

Available operations (selectable from the dropdown menu) include the **basic arithmetic operators**.  
Division and square root extraction, since only integer values ​​are allowed in the program, are returned only as integer values.
Additionally, **modulo** and **bitwise** operators are available.

For the **bitwise NOT** operation, only the **third parameter** is used.  
However, due to backend implementation, a **second parameter must still be provided**, even though it is ignored.  
This means you must enter a placeholder value for the second parameter when using bitwise NOT — it has no effect on the result but is required for proper execution.

---

## Time
![Time Blocks](static/software_info/images/time_block.png)
Time blocks allow you to **pause program execution** for a specific duration.  
Two blocks are available, differing only in their **time units**.

---

## Debug
![Debug Block](static/software_info/images/debug_block.png)
Currently, there is one debug block.  
It outputs the specified value to the **local (frontend) console**, allowing users to monitor values, calculations, and the program flow for debugging purposes.