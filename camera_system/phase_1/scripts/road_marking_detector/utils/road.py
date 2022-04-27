import numpy as np

ROAD_CLASSES_LIST = [
	'unlabeled',
	'SA', 
	'LA',
	'RA',
	'SLA', 
	'SRA',
	'JB', 
	'PC', 
	'DM',
	'SL', 
	'BL', 
	'CL',
]


ROAD_CLASSES_SET = set(ROAD_CLASSES_LIST)

ROAD_CLASS_ID = {
    cls_name: idx for idx, cls_name in enumerate(ROAD_CLASSES_LIST)
}

# Random RGB colors for each class (useful for drawing bounding boxes)
ROAD_COLORS = \
    np.random.uniform(0, 255, size=(len(ROAD_CLASSES_LIST), 3)).astype(np.uint8)


def is_road_label(label):
    """Returns boolean which tells if given label is ROAD label.

    Args:
        label (str): object label
    Returns:
        bool: is given label a ROAD class label
    """
    return label in ROAD_CLASSES_SET

def get_road_label_color(label):
    """Returns color corresponding to given ROAD label, or None.

    Args:
        label (str): object label
    Returns:
        np.array: RGB color described in 3-element np.array
    """
    if not is_road_label(label):
        return None
    else:
        return ROAD_COLORS[ROAD_CLASS_ID[label]]
