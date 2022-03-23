import xml.etree.ElementTree as ET
import numpy as np
import os


root_file_dir = 'D:\\ACA\\fyp\\codes\\remove_small_bboxes\\xml_files\\test_2'
root_edited_file_dir = 'D:\\ACA\\fyp\\codes\\remove_small_bboxes\\edited_xml_files\\test_2'


traffic_light_min_width = 6
traffic_light_min_height = 6

count_down_min_width = 6
count_down_min_height = 6

sub_dirs = ["narrow","wide"]
# narrow_file_dir = os.path.join(root_file_dir,"narrow")
# wide_file_dir = os.path.join(root_file_dir,"wide")

# narrow_edited_file_dir = os.path.join(root_edited_file_dir,"narrow")
# wide_edited_file_dir = os.path.join(root_edited_file_dir,"wide")



edited_file_count = 0
popped_bbox_count = 0

def pop_small_bboxes(file_name,file_dir,edited_file_dir):

    global edited_file_count,popped_bbox_count
    file_edited = False

    fn_xml = os.path.join(file_dir, file_name)
    fn_xml = fn_xml.replace('\\','/')
    # with open(fn_xml) as fn:
    tree = ET.parse(fn_xml)
    root = tree.getroot()

    for child in root.findall(".//object"):
        for grandChild in child:
            if (grandChild.tag == 'name'):
                name = grandChild.text
            elif(grandChild.tag == 'bndbox'):
                    for coord in grandChild:
                        if(coord.tag == 'xmin'):
                            x_1 = float(coord.text)
                            coord.text = str(x_1)
                        if(coord.tag == 'ymin'): 
                            y_1 = float(coord.text)
                            coord.text = str(y_1)
                        if(coord.tag == 'xmax'): 
                            x_2 = float(coord.text)
                            coord.text = str(x_2)
                        if(coord.tag == 'ymax'): 
                            y_2 = float(coord.text)
                            coord.text = str(y_2)
        l1 = abs(x_2-x_1)
        l2 = abs(y_2-y_1)
        width = min(l1,l2)
        height = max(l1,l2)

        if ((name == "Count-down") or (name == "empty-count-down")):
            if ((width < count_down_min_width) or (height < count_down_min_height)):
                print("detected small count down box",child.tag)
                root.remove(child)
                popped_bbox_count += 1
                file_edited = True
        else:
            if ((width < traffic_light_min_width) or (height < traffic_light_min_height)):
                print("detected small traffic light",child.tag)
                root.remove(child)
                popped_bbox_count += 1
                file_edited = True
    
    out_xml = os.path.join(edited_file_dir, file_name)
    out_xml = out_xml.replace('\\','/')
    tree.write(out_xml,short_empty_elements=False)   
    if (file_edited):
        edited_file_count += 1


for sub_dir in sub_dirs:
    file_dir = os.path.join(root_file_dir,sub_dir)
    edited_file_dir = os.path.join(root_edited_file_dir,sub_dir)
    arr_xml_filenames = []

    if not(os.path.isdir(edited_file_dir)):
        os.mkdir(edited_file_dir)
    for f in os.listdir(file_dir):
        if f.endswith(".xml"):
            arr_xml_filenames.append(f)    

    for fn in arr_xml_filenames:
        pop_small_bboxes(fn,file_dir,edited_file_dir)
        # break

print("edited file count:",edited_file_count)
print("removed bbox count:", popped_bbox_count)