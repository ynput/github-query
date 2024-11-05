# Changelog

### **Enhancement**

<details>
<summary>Improve applying render resolution and aspect ratio on render settings reset - <a href="https://github.com/ynput/ayon-maya/pull/75")>#75</a></summary>


Fix pixel aspect ratio / device aspect ratio getting messed up for Arnold renderer on render settings reset.

Additionally:
- This now applies the resolution from the task entity, not the folder entity.
- This now also applies pixel aspect ratio as defined on the entity.

___

</details>
<details>
<summary>Validate unique names only within the instance not in full scene - <a href="https://github.com/ynput/ayon-maya/pull/70")>#70</a></summary>


Validate unique names only within the instance not in full scene

___

</details>

### **Bug**

<details>
<summary>AY-6654 Look: Fix None values in collecting and applying attributes - <a href="https://github.com/ynput/ayon-maya/pull/89")>#89</a></summary>


This fixes a case where looks failed to apply due to `None` values being present in the collected attributes.
These will now be ignored in collected. There's an edge case where Maya returns `None` for string attributes that have no values set - those are captured now explicitly to just `""` to still collect and apply them later.

Existing looks will now also apply correctly with `None` value in their look attributes, but the attributes with `None` values will be ignored with a warning.

___

</details>
<details>
<summary>Fix settings for Maya USD Animation Extractor - <a href="https://github.com/ynput/ayon-maya/pull/77")>#77</a></summary>


Fix name in settings to match with name of plug-in to ensure settings are actually applied

___

</details>
<details>
<summary>Improve applying render resolution and aspect ratio on render settings reset - <a href="https://github.com/ynput/ayon-maya/pull/75")>#75</a></summary>


Fix pixel aspect ratio / device aspect ratio getting messed up for Arnold renderer on render settings reset.

Additionally:
- This now applies the resolution from the task entity, not the folder entity.
- This now also applies pixel aspect ratio as defined on the entity.

___

</details>
<details>
<summary>Maya Scene exports do not default to including nodes that not children of members - <a href="https://github.com/ynput/ayon-maya/pull/71")>#71</a></summary>


On Maya scene exports only include the relevant history for the selected nodes downstream and upstream and not upstream, and also their downstream descendant children.

___

</details>

### **Maintenance**

<details>
<summary>Skip extraction of active view for automatic tests - <a href="https://github.com/ynput/ayon-maya/pull/126")>#126</a></summary>

It seems that Maya UI is not completely visible or shutting down, `view.readColorBuffer` causes RuntimeError: (kFailure): Unexpected Internal Failure aas view is not visible.

___

</details>
