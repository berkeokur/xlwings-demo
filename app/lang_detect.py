from polyglot.detect import Detector

def detect_language_polyglot(text):
    try:
        detector = Detector(text)
        detected_language = detector.language.code
        confidence = detector.language.confidence
        return detected_language, confidence
    except Exception as e:
        print("An error occurred:", e)
        return None, 0.0
