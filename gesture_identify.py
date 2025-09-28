import numpy as np

def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def classify_hand(landmarks):

    if not landmarks or len(landmarks) < 21:
        return 'unknown_gesture'
    
    try:

        points = {lm[0]: (lm[1], lm[2]) for lm in landmarks}
        
        finger_tips = {
            'thumb': 4,
            'index': 8,
            'middle': 12,
            'ring': 16,
            'pinky': 20
        }
        
        finger_pips = {
            'thumb': 2,
            'index': 6,
            'middle': 10,
            'ring': 14,
            'pinky': 18
        }
        
        extended_fingers = []
        
        thumb_tip = points.get(4)
        thumb_ip = points.get(3)
        if thumb_tip and thumb_ip:
            # For right hand: thumb is extended when tip is to the right of IP joint (higher x coordinate)
            if thumb_tip[0] > thumb_ip[0]:
                extended_fingers.append('thumb')
        
        # Check if the other four fingers are extended (tip above PIP joint)
        for finger, tip_id in finger_tips.items():
            if finger == 'thumb':
                continue
                
            pip_id = finger_pips[finger]
            tip = points.get(tip_id)
            pip = points.get(pip_id)
            
            if tip and pip:
                # Finger extended: tip y coordinate less than PIP joint y coordinate
                # Relaxed condition: allow slight bending
                if tip[1] < pip[1] + 20:  # Add 20 pixel tolerance
                    extended_fingers.append(finger)
        
        # Classify gesture based on extended fingers (more lenient logic)
        num_extended = len(extended_fingers)
        
        # Rock (fist): 0-1 fingers extended
        if num_extended <= 1:
            return 'fist'
        # Scissors: 2-3 fingers extended, including index and middle
        elif 2 <= num_extended <= 3 and 'index' in extended_fingers and 'middle' in extended_fingers:
            return 'scissor'
        # Paper: 3 or more fingers extended
        elif num_extended >= 3:
            return 'paper'
        else:
            return 'unknown_gesture'
            
    except Exception as e:
        print(f"Gesture recognition error: {e}")
        return 'unknown_gesture'

# Test function
def test_gesture_recognition():
    """Test gesture recognition functionality"""
    
    # Example landmarks for rock gesture (all fingers curled)
    fist_landmarks = [
        [0, 320, 400], [1, 310, 380], [2, 300, 360], [3, 290, 340], [4, 280, 320],
        [5, 330, 380], [6, 340, 360], [7, 350, 340], [8, 360, 320],
        [9, 360, 380], [10, 370, 360], [11, 380, 340], [12, 390, 320],
        [13, 390, 380], [14, 400, 360], [15, 410, 340], [16, 420, 320],
        [17, 420, 380], [18, 430, 360], [19, 440, 340], [20, 450, 320]
    ]
    
    # Example landmarks for scissors gesture (index and middle fingers extended)
    scissors_landmarks = [
        [0, 320, 400], [1, 310, 380], [2, 300, 360], [3, 290, 340], [4, 280, 320],
        [5, 330, 380], [6, 340, 360], [7, 350, 340], [8, 360, 280],  # index extended
        [9, 360, 380], [10, 370, 360], [11, 380, 340], [12, 390, 280], # middle extended
        [13, 390, 380], [14, 400, 360], [15, 410, 340], [16, 420, 320],
        [17, 420, 380], [18, 430, 360], [19, 440, 340], [20, 450, 320]
    ]
    
    # Example landmarks for paper gesture (all fingers extended)
    paper_landmarks = [
        [0, 320, 400], [1, 310, 380], [2, 300, 360], [3, 290, 340], [4, 280, 280],
        [5, 330, 380], [6, 340, 360], [7, 350, 340], [8, 360, 280],
        [9, 360, 380], [10, 370, 360], [11, 380, 340], [12, 390, 280],
        [13, 390, 380], [14, 400, 360], [15, 410, 340], [16, 420, 280],
        [17, 420, 380], [18, 430, 360], [19, 440, 340], [20, 450, 280]
    ]
    
    print("Testing gesture recognition:")
    print(f"Rock: {classify_hand(fist_landmarks)}")
    print(f"Scissors: {classify_hand(scissors_landmarks)}")
    print(f"Paper: {classify_hand(paper_landmarks)}")

if __name__ == "__main__":
    test_gesture_recognition()