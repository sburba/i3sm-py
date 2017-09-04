# i3sm-py
This is an alternative movement scheme for i3.

It differs from the default i3 movement in two ways:
1. Never wrap around containers
2. When moving into a split container, focus the window in that container closest to the top left of the current container


# Install
1. Download the latest release from the releases page.
2. Unzip it and place the binary somewhere in your path
3. In your i3 config file, replace all occurrances of `focus <direction>` with `exec i3sm <direction>`

# Building
```bash
pip3 install -r requirements.txt
./build_release.sh
```
The executable will be placed the dist folder

# Rationale

The reasons for and against wrapping around containers are pretty self explanatory, I prefer no wrapping so that's what this
implementation does

For moving into split containers, the default behavior is to focus the window in the container that most recently had focus.
This means that in order to know which window is going to get focus you have to remember which window in that container was
focused last, which could been last focused hours ago.

It's easier to explain with an example; suppose you have this layout (the container number with the stars around it is focused):
```
+-------+-------+
|       |       |
|  *1*  |   2   |
|       |       |
+---------------+
|       |       |
|   3   |   4   |
|       |       |
+-------+-------+
```
The default movement system the commands 
```bash
i3-msg focus right
i3-msg focus down
i3-msg focus left
```
will result in the following movements

```
+-------+-------+
|       |       |
|   1   |  *2*  |
|       |       |
+---------------+
|       |       |
|   3   |   4   |
|       |       |
+-------+-------+
+-------+-------+
|       |       |
|   1   |   2   |
|       |       |
+---------------+
|       |       |
|   3   |  *4*  |
|       |       |
+-------+-------+
+-------+-------+
|       |       |
|  *1*  |   2   |
|       |       |
+---------------+
|       |       |
|   3   |   4   |
|       |       |
+-------+-------+
```
But the i3sm commands
```bash
i3sm right
i3sm down
i3sm left
```
Will result in the following movements
```
+-------+-------+
|       |       |
|   1   |  *2*  |
|       |       |
+---------------+
|       |       |
|   3   |   4   |
|       |       |
+-------+-------+
+-------+-------+
|       |       |
|   1   |   2   |
|       |       |
+---------------+
|       |       |
|   3   |  *4*  |
|       |       |
+-------+-------+
+-------+-------+
|       |       |
|   1   |   2   |
|       |       |
+---------------+
|       |       |
|  *3*  |   4   |
|       |       |
+-------+-------+
```
