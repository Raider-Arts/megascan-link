
# How to use the plugin


## Download the plugin

You can find it in the [realease](https://github.com/Raider-Arts/megascan-link/releases) tab of the github project 

or in the Substance

##### **Build types:**
- Development Buid
    > This build is always updated as soon a commit is pushed on the master branch
    ```eval_rst
    .. warning::
        This builds can be very unstable or not working at all!
        So when use them expect them to not work or not behaving correctly
    ```

- Tagged Buils
    > The tagged builds are stable usable builds

## Install the plugin
Install it in Substance Designer using the Plugin manager, you can find it under ``Tools > Plugin Manager..`` then click ``install`` and navigate to the path were you previously downloaded it

```eval_rst
.. note::
    Refere to the official doc for installing a `Plugin Package <https://docs.substance3d.com/sddoc/plugins-packages-182257045.html>`_
```

## Use the Plugin
After you have installed the plugin go to **Quixel Bridge** select the **Megascan asset** you want to import on Substance Designer go to the **Export Setting** tab and select from the **Export To** drop down the **Custom Socket Export** option, then in the **Socket Port** insert the same port you have set up on the **Plugin Settings** (Default to **24891**) 

##### Bridge setup example
![Bridge setup example](_static/megascan_setup.gif)

##### Substance designer import step
![Bridge setup example](_static/designer_import.gif)

## Plugin Settings
A new icon appeared in the SUbstance Designer toolbar, that icon button opens the Plugin settigns dialogs as shown in the 