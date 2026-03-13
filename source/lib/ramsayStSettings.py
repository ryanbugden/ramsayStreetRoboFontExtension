import ezui

from mojo.roboFont import OpenWindow
from mojo.UI import PutFile, GetFile
from mojo.events import postEvent

import ramsayStData
from importlib import reload as reloadlib
reloadlib(ramsayStData)
from ramsayStData import RamsayStData



class RamsayStSettingsController(ezui.WindowController):

    def build(self):
        content = """
        * TwoColumnForm                 @form
        
        > : Show:
        > [X] Edit Mode                 @showNeighborsEditMode
        > [X] Preview Mode              @showNeighborsPreviewMode
        
        > : Fill Color:
        > * HorizontalStack             @colorStack
        >> * ColorWell                  @fillColorLight
        >> * ColorWell                  @fillColorDark
        
        > : Stroke Color:
        > * HorizontalStack             @colorStack
        >> * ColorWell                  @strokeColorLight
        >> * ColorWell                  @strokeColorDark
        
        > :
        > * HorizontalStack
        >> Light                        @lightLabel
        >> Dark                         @darkLabel
        
        
        # > : Stroke Color:
        # > * ColorWell                 @strokeColor
        
        ---
        
        |-----------------------------|
        | left   | glyph   | right    | @table
        |--------|---------|----------|
        | A      | A       | A        |
        |        |         |          |
        |-----------------------------|
        > (+-)                          @tableAddRemove
        > (Import)                      @importButton
        > (Export)                      @exportButton
        """
        column_width = 80
        padding = 28
        form_title_width = column_width + 14
        form_item_width = column_width*3 - form_title_width + padding*2
        button_width = (form_item_width - 10) / 2
        descriptionData = dict(
            form=dict(
                titleColumnWidth=column_width + 14,
                itemColumnWidth=form_item_width,
            ),
            table=dict(
                width="fill",
                height="fill",
                items=RamsayStData.getItems(),
                columnDescriptions=[
                    dict(
                        identifier="left",
                        title="Left",
                        width=column_width,
                        editable=True
                    ),
                    dict(
                        identifier="glyph_name",
                        title="Glyph Name",
                        width=column_width,
                        editable=True
                    ),
                    dict(
                        identifier="right",
                        title="Right",
                        width=column_width,
                        editable=True
                    ),
                ]
            ),
            colorStack=dict(
                distribution="fillEqually",
            ),
            fillColorLight=dict(
                color=(0,0,1,0.2),
                width=button_width,
                height=20,
            ),
            fillColorDark=dict(
                color=(0,0,1,0.2),
                width=button_width,
                height=20,
            ),
            strokeColorLight=dict(
                color=(0,0,1,0),
                width=button_width,
                height=20,
            ),
            strokeColorDark=dict(
                color=(0,0,1,0),
                width=button_width,
                height=20,
            ),
            lightLabel=dict(
                width=button_width,
                sizeStyle="mini",
            ),
            darkLabel=dict(
                width=button_width,
                sizeStyle="mini",
            ),
            importButton=dict(
                width=button_width
            ),
            exportButton=dict(
                width=button_width
            ),
        )
        self.w = ezui.EZPanel(
            title="Ramsay St.",
            size=(column_width*3, 400),
            minSize=(column_width*3, 300),
            maxSize=(column_width*3, 800),
            content=content,
            descriptionData=descriptionData,
            controller=self
        )

    def started(self):
        self.w.open()

    def formCallback(self, sender):
        print("formCallback")
        self.update()

    def tableEditCallback(self, sender):
        self.update()
        
    def tableAddRemoveButtonAddCallback(self, sender):
        table = self.w.getItem("table")
        item = table.makeItem(
            left="A",
            glyph_name="A",
            right="A"
        )
        table.appendItems([item])
        self.update()

    def tableAddRemoveButtonRemoveCallback(self, sender):
        table = self.w.getItem("table")
        table.removeSelectedItems()
        self.update()

    def update(self):
        RamsayStData.fillColorLight = self.w.getItem("fillColorLight").get()
        RamsayStData.fillColorDark = self.w.getItem("fillColorDark").get()
        RamsayStData.strokeColorLight = self.w.getItem("strokeColorLight").get()
        RamsayStData.strokeColorDark = self.w.getItem("strokeColorDark").get()
        RamsayStData.showNeighbours = self.w.getItem("showNeighborsEditMode").get()
        RamsayStData.showPreview = self.w.getItem("showNeighborsPreviewMode").get()
        RamsayStData.data = self.w.getItem("table").get()
        RamsayStData.save()
        postEvent(RamsayStData.changedEventName)
        
    def importGlyphNames(self):
        path = GetFile(
            message="Where would you like to import Ramsay St. settings from?", 
            title="Import Ramsay St. Settings",
            allowsMultipleSelection=False, 
            fileTypes=["ramsaySt"], 
            parentWindow=self.w, 
        )
        if path:
            path = path[0]
            with open(path, "r") as blob:
                lines = blob.read().splitlines()

            data = dict()
            for line in lines:
                if line.startswith("#"):
                    continue

                items = line.split()
                if len(items) == 3:
                    glyphName, leftGlyphName, rightGlyphName = items
                    if leftGlyphName == '_':
                        leftGlyphName = ' '
                    if rightGlyphName == '_':
                        rightGlyphName = ' '
                    data["glyph_name"] = glyphName
                    data["left"] = leftGlyphName
                    data["right"] = rightGlyphName
                else:
                    continue

            RamsayStData.clear()
            RamsayStData.update(data)
            self.w.table.set(data)
            self.update()

    def importGlyphNames(self, path):
        if path:
            path = path[0]
            with open(path, "r") as blob:
                lines = blob.read().splitlines()

            data = dict()
            for line in lines:
                if line.startswith("#"):
                    continue

                items = line.split()
                if len(items) == 3:
                    glyphName, leftGlyphName, rightGlyphName = items
                    if leftGlyphName == '_':
                        leftGlyphName = ' '
                    if rightGlyphName == '_':
                        rightGlyphName = ' '
                    data[glyphName] = leftGlyphName, rightGlyphName
                else:
                    continue

            RamsayStData.clear()
            RamsayStData.update(data)
            self.w.dataList.set(RamsayStData.getItems())
            self.update()

    def exportGlyphNames(self):
        path = PutFile(
            message="Where would you like to save these Ramsay St. settings?", 
            fileName="Untitled.ramsaySt",   
            parentWindow=self.w, 
        )
        if path is None:
            return

        output = [
            "# Ramsay St. Glyph List",
            "# Use _ as a placeholder for 'no glyph'",
            "# <glyphName> <leftGlyphName> <rightGlyphName>"
        ]
        for dataEntry in RamsayStData.data:
            left, glyphName, right = dataEntry["left"], dataEntry["glyph_name"], dataEntry["right"]
            if all([left is not None, right is not None]):
                if left in (' ', ''):
                    left = '_'
                if right in (' ', ''):
                    right = '_'
                output.append(f"{glyphName} {left} {right}")

        with open(path, "w") as blob:
            blob.write("\n".join(output))


RamsayStSettingsController()
