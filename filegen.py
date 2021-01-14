#import srctools
from zipfile import ZipFile

# Script to generate info.txt and editoritems.txt

def _genInfoStr(ucp):
    temp = f'''//Created with UCP-UI
"ID"    "{ucp['id']}"
"Name"  "{ucp['title']}"
"Desc"  "{ucp['description']}"


'''
    for item in ucp['items']:
        temp += '''
"Item"
    {{
    "ID"    "{itemId}"
    "Version"
        {{
        "Styles"
            {{
            "BEE2_CLEAN"    "{itemId}"
            }}
        }}
    }}
'''.format(itemId = item['id'])
    return temp

def _genEditoritemsStr(ucp,item):
    return '''"Item"
{{
    "Type"  "{itemName}"
    "ItemClass"	"ItemButtonFloor"
    "Editor"
    {{
        "SubType"
        {{
            "Name"  "{itemName}"
            "Model"
            {{
                "ModelName" "sentry.3ds"
            }}
            "Palette"
            {{
                "Tooltip"   "{itemNameUpper}"
                "Image"     "palette/BEE2/{packageId}/{itemId}.png"
            }}
            "Sounds"
            {{
                "SOUND_CREATED"					"P2Editor.PlaceOther"
				"SOUND_EDITING_ACTIVATE"		"P2Editor.ExpandOther"
				"SOUND_EDITING_DEACTIVATE"		"P2Editor.CollapseOther"
				"SOUND_DELETED"					"P2Editor.RemoveOther"
            }}
        }}
        "MovementHandle"    "{handleType}"
        "DesiredFacing"     "{desiredFacing}"
        "InvalidSurface"    "{surfaces}"
    }}
    "Properties"
    {{
    }}
    "Exporting"
    {{
        "Instances"
        {{
            "0"
            {{
                "Name"  "instances/BEE2/{packageId}/{itemId}_0.vmf"
                "EntityCount"		"0"
				"BrushCount"		"0"
				"BrushSideCount"	"0"
            }}
        }}
        "Offset"    "64 64 64"
        "OccupiedVoxels"
		{{
			"Volume"
			{{
				"Pos1"		"0 0 0"
				"Pos2"		"1 1 1"
				"Surface"
				{{
					"Normal"	"0 0 1"
				}}
			}}
		}}
        "EmbeddedVoxels"
        {{

        }}
    }}
}}
'''.format( itemName = item['title'],
            itemId = item['id'],
            itemNameUpper = item['title'].upper(),
            packageId = ucp['id'],
            surfaces = ' '.join([['CEIL','FLOOR','WALL'][x] for x,y in enumerate(item['placement']) if not int(y)]),
            handleType = item['handle'],
            desiredFacing = item['orientation']
    )

def _genPropertiesStr(ucp,item):
    return '''
"Properties"
{{
"Authors"     "{{authors}}"
"Tags"        "UCP-UI"

"ent_count"   "0"
"Icon"
	{{
	"0"   "{packageId}/{itemId}.png"
	}}
}}
'''.format( itemId = item['id'],
            #authors = ucp['authors'],
            packageId = ucp['id']
)

def genFiles(ucp,zipname):
    with ZipFile(zipname,'w') as file:
        file.writestr('info.txt',_genInfoStr(ucp))
        for item in ucp['items']:
            file.writestr(f'items/{item["id"]}/editoritems.txt',_genEditoritemsStr(ucp,item))
            file.writestr(f'items/{item["id"]}/properties.txt',_genPropertiesStr(ucp,item))
