import streamlit as st
import pandas as pd
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime

# Initialize or load stored return data
if "return_data" not in st.session_state:
    st.session_state.return_data = {}

st.set_page_config(page_title="Vimochana System", layout="centered")
st.title("♻️ Vimochana QR Scanner")
st.markdown("Return plastic, scan QR code, and get ₹10 back!")

# Function to scan QR from webcam
def scan_qr():
    cap = cv2.VideoCapture(0)
    st.info("📷 Press 'q' to quit scanning.")
    scanned_id = None

    while True:
        success, frame = cap.read()
        if not success:
            st.error("Could not access webcam.")
            break

        # Detect and decode QR codes
        qrcodes = decode(frame)
        for qr in qrcodes:
            scanned_id = qr.data.decode("utf-8")
            cv2.rectangle(frame, (qr.rect.left, qr.rect.top),
                          (qr.rect.left + qr.rect.width, qr.rect.top + qr.rect.height),
                          (0, 255, 0), 2)
            cv2.putText(frame, scanned_id, (qr.rect.left, qr.rect.top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # Display frame in a window (external)
        cv2.imshow("Scan QR Code - Press 'q' to exit", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or scanned_id is not None:
            break

    cap.release()
    cv2.destroyAllWindows()

    return scanned_id

# Button to trigger scanner
if st.button("🎥 Start QR Scan"):
    qr_id = scan_qr()

    if qr_id:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if qr_id not in st.session_state.return_data:
            st.session_state.return_data[qr_id] = {
                "returned": True,
                "time": now,
                "amount": 10
            }
            st.success(f"✅ Returned {qr_id}! ₹10 added on {now}")
            st.write("Receipt:")
            st.json(st.session_state.return_data[qr_id])
        else:
            st.warning("⚠️ This item has already been returned.")
            st.write("Previous receipt:")
            st.json(st.session_state.return_data[qr_id])
    else:
        st.error("No QR code detected.")

# View all logged returns
if st.button("📄 View All Returns"):
    st.write(pd.DataFrame.from_dict(st.session_state.return_data, orient='index'))
