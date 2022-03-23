import numpy as np

TRAFFIC_CLASSES_LIST = [
	'unlabeled',
	'PRS', 
	'OSD',
	'PHS',
	'MNS', 
	'APR',
	'SLS', 
	'TLS', 
	'DWS',
	
]


TRAFFIC_CLASSES_SET = set(TRAFFIC_CLASSES_LIST)

TRAFFIC_CLASS_ID = {
    cls_name: idx for idx, cls_name in enumerate(TRAFFIC_CLASSES_LIST)
}

# Random RGB colors for each class (useful for drawing bounding boxes)
TRAFFIC_COLORS = \
    np.random.uniform(0, 255, size=(len(TRAFFIC_CLASSES_LIST), 3)).astype(np.uint8)


def is_traffic_label(label):
    """Returns boolean which tells if given label is TRAFFIC label.

    Args:
        label (str): object label
    Returns:
        bool: is given label a TRAFFIC class label
    """
    return label in TRAFFIC_CLASSES_SET

def get_traffic_label_color(label):
    """Returns color corresponding to given TRAFFIC label, or None.

    Args:
        label (str): object label
    Returns:
        np.array: RGB color described in 3-element np.array
    """
    if not is_traffic_label(label):
        return None
    else:
        return TRAFFIC_COLORS[TRAFFIC_CLASS_ID[label]]
