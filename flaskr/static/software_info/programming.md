# Programming
The programming interface is designed to work similarly to **Scratch**.
Program execution runs **from top to bottom**.

To create a program, simply **drag a block** into the workspace.
Blocks are automatically arranged starting from the **top-left corner** of the workspace — manual positioning is not possible.

![Run Button](static/software_info/images/run.png)
The program can be started using the **“Run”** button.

![Delete Button](static/software_info/images/delete.png)
To remove all blocks from the workspace, use the **“Delete Everything”** button.

![Delete block](static/software_info/images/delete_blocks.png)
When scrolling down in the workspace, a **delete area** appears.
You can drag and drop blocks into this area to remove them from the workspace.

There are a few additional details to consider when programming:

---

## Special Notes

### Variables

It will always result in an **error** if a variable or position variable is placed **alone** in the workspace.
Variables must always be **assigned to a block** and cannot stand independently.

---

### Subprograms (Child Blocks)

![Nested Block](static/software_info/images/nested_block.png)
All **`Control` blocks** can contain **sub-blocks**, also called **child blocks**.
These child blocks can only be added within the workspace.

To add a child block, **drag a block** and **drop it directly onto** the desired control block.
The dropped block will then automatically become its child.
You can also nest additional `Control` blocks inside others, allowing multiple levels of **nested child blocks**.