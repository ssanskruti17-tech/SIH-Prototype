import os
import streamlit as st

from ocr import run_ocr, get_average_confidence
from parser import parse_product
from validator import validate_product

from history import (
    load_history,
    save_scan,
    create_scan_id
)


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="LabelGuard",
    page_icon="🔍",
    layout="wide"
)


# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .history-card {
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "page" not in st.session_state:

    st.session_state.page = "scan"


if "selected_scan" not in st.session_state:

    st.session_state.selected_scan = None


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🔍 LabelGuard")

    st.divider()

    # Scan Product
    if st.button(
        "📷 Scan Product",
        use_container_width=True
    ):

        st.session_state.page = "scan"

        st.session_state.selected_scan = None

    # History
    if st.button(
        "📚 History",
        use_container_width=True
    ):

        st.session_state.page = "history"

        st.session_state.selected_scan = None

    st.divider()

    st.caption(
        "AI-Assisted Packaged Commodity "
        "Label Compliance Prototype"
    )


# ==================================================
# HISTORY PAGE
# ==================================================

if st.session_state.page == "history":

    st.title("📚 Scan History")

    history = load_history()

    if not history:

        st.info(
            "No products have been scanned yet."
        )

    else:

        st.write(
            f"Total scans: **{len(history)}**"
        )

        st.divider()

        for scan in history:

            scan_id = scan["scan_id"]

            date = scan["date"]

            status = scan["status"]

            product = scan["product"]

            if status == "COMPLIANT":

                status_icon = "✅"

            else:

                status_icon = "⚠️"

            st.markdown(
                f"""
                ### {status_icon} Scan {scan_id}

                **Date:** {date}

                **MRP:** {product.get("mrp") or "Not detected"}

                **Quantity:** {product.get("quantity") or "Not detected"}

                **Status:** {status}
                """
            )

            if st.button(
                "View Scan",
                key=f"view_{scan_id}"
            ):

                st.session_state.selected_scan = scan

            st.divider()


    # ----------------------------------------------
    # SHOW SELECTED SCAN
    # ----------------------------------------------

    if st.session_state.selected_scan:

        scan = st.session_state.selected_scan

        st.subheader("🔎 Scan Details")

        col1, col2 = st.columns(2)

        with col1:

            st.write("### 📷 Front Image")

            if os.path.exists(
                scan["front_image"]
            ):

                st.image(
                    scan["front_image"],
                    use_container_width=True
                )

        with col2:

            st.write("### 📷 Back Image")

            if os.path.exists(
                scan["back_image"]
            ):

                st.image(
                    scan["back_image"],
                    use_container_width=True
                )

        st.divider()

        product = scan["product"]

        st.subheader(
            "📄 Extracted Declarations"
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "MRP",
                product.get("mrp")
                or "Not detected"
            )

        with c2:
            st.metric(
                "Net Quantity",
                product.get("quantity")
                or "Not detected"
            )

        with c3:
            st.metric(
                "Manufacturer",
                product.get("manufacturer")
                or "Not detected"
            )

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Importer",
                product.get("importer")
                or "Not detected"
            )

        with c2:
            st.metric(
                "Consumer Care",
                product.get("consumer_care")
                or "Not detected"
            )

        st.divider()

        if scan["status"] == "COMPLIANT":

            st.success("✅ COMPLIANT")

        else:

            st.warning("⚠️ NEEDS REVIEW")

        if scan["issues"]:

            st.subheader(
                "⚠️ Potential Issues"
            )

            for issue in scan["issues"]:

                st.error(issue)


# ==================================================
# SCAN PRODUCT PAGE
# ==================================================

else:

    st.markdown(
        '<div class="main-title">'
        '🔍 LabelGuard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-Assisted Packaged Commodity '
        'Label Compliance Prototype'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader(
        "📷 Scan Product"
    )

    st.write(
        "Upload both the **front** and "
        "**back** images of the package."
    )

    # ----------------------------------------------
    # FRONT + BACK UPLOAD
    # ----------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### 📷 Front Side"
        )

        front_image = st.file_uploader(
            "Upload Front Image",
            type=[
                "jpg",
                "jpeg",
                "png"
            ],
            key="front"
        )

    with col2:

        st.markdown(
            "### 📷 Back Side"
        )

        back_image = st.file_uploader(
            "Upload Back Image",
            type=[
                "jpg",
                "jpeg",
                "png"
            ],
            key="back"
        )


    # ----------------------------------------------
    # PREVIEW
    # ----------------------------------------------

    if front_image or back_image:

        st.divider()

        st.subheader(
            "👀 Image Preview"
        )

        col1, col2 = st.columns(2)

        with col1:

            if front_image:

                st.image(
                    front_image,
                    caption="Front Side",
                    use_container_width=True
                )

        with col2:

            if back_image:

                st.image(
                    back_image,
                    caption="Back Side",
                    use_container_width=True
                )


    # ----------------------------------------------
    # SCAN BUTTON
    # ----------------------------------------------

    st.divider()

    scan_button = st.button(
        "🚀 Scan Product",
        use_container_width=True,
        type="primary"
    )


    if scan_button:

        if not front_image:

            st.error(
                "Please upload the front image."
            )

            st.stop()

        if not back_image:

            st.error(
                "Please upload the back image."
            )

            st.stop()


        # ------------------------------------------
        # CREATE SCAN ID
        # ------------------------------------------

        scan_id = create_scan_id()

        os.makedirs(
            "uploads",
            exist_ok=True
        )


        # ------------------------------------------
        # SAVE IMAGES
        # ------------------------------------------

        front_path = os.path.join(
            "uploads",
            f"{scan_id}_front.jpg"
        )

        back_path = os.path.join(
            "uploads",
            f"{scan_id}_back.jpg"
        )


        with open(
            front_path,
            "wb"
        ) as file:

            file.write(
                front_image.getbuffer()
            )


        with open(
            back_path,
            "wb"
        ) as file:

            file.write(
                back_image.getbuffer()
            )


        # ------------------------------------------
        # OCR FRONT
        # ------------------------------------------

        with st.spinner(
            "🔎 Scanning front image..."
        ):

            try:

                front_ocr = run_ocr(
                    front_path
                )

            except Exception as e:

                st.error(
                    "Front image OCR failed."
                )

                st.exception(e)

                st.stop()


        # ------------------------------------------
        # OCR BACK
        # ------------------------------------------

        with st.spinner(
            "🔎 Scanning back image..."
        ):

            try:

                back_ocr = run_ocr(
                    back_path
                )

            except Exception as e:

                st.error(
                    "Back image OCR failed."
                )

                st.exception(e)

                st.stop()


        # ------------------------------------------
        # COMBINE OCR
        # ------------------------------------------

        all_ocr = (
            front_ocr +
            back_ocr
        )


        # ------------------------------------------
        # PARSE
        # ------------------------------------------

        with st.spinner(
            "🧠 Extracting product information..."
        ):

            product = parse_product(
                all_ocr
            )


        # ------------------------------------------
        # VALIDATE
        # ------------------------------------------

        validation = validate_product(
            product,
            all_ocr
        )


        # ------------------------------------------
        # CONFIDENCE
        # ------------------------------------------

        average_confidence = (
            get_average_confidence(all_ocr)
        )


        # ------------------------------------------
        # SAVE TO HISTORY
        # ------------------------------------------

        from datetime import datetime

        scan_data = {

            "scan_id": scan_id,

            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "front_image": front_path,

            "back_image": back_path,

            "product": product,

            "status": validation["status"],

            "issues": validation["issues"],

            "ocr_confidence": average_confidence
        }


        save_scan(scan_data)


        # ------------------------------------------
        # DISPLAY RESULT
        # ------------------------------------------

        st.divider()

        st.subheader(
            "📊 Compliance Result"
        )


        if validation["status"] == "COMPLIANT":

            st.success(
                "✅ COMPLIANT"
            )

        else:

            st.warning(
                "⚠️ NEEDS REVIEW"
            )


        # ------------------------------------------
        # DECLARATIONS
        # ------------------------------------------

        st.subheader(
            "📄 Extracted Declarations"
        )


        c1, c2, c3 = st.columns(3)


        with c1:

            st.metric(
                "MRP",
                product["mrp"]
                or "Not detected"
            )


        with c2:

            st.metric(
                "Net Quantity",
                product["quantity"]
                or "Not detected"
            )


        with c3:

            st.metric(
                "Manufacturer",
                product["manufacturer"]
                or "Not detected"
            )


        c1, c2 = st.columns(2)


        with c1:

            st.metric(
                "Importer",
                product["importer"]
                or "Not detected"
            )


        with c2:

            st.metric(
                "Consumer Care",
                product["consumer_care"]
                or "Not detected"
            )


        # ------------------------------------------
        # CONFIDENCE
        # ------------------------------------------

        st.subheader(
            "🎯 OCR Confidence"
        )

        st.progress(
            min(
                max(
                    average_confidence,
                    0
                ),
                1
            )
        )

        st.write(
            f"Average OCR confidence: "
            f"**{average_confidence * 100:.2f}%**"
        )


        # ------------------------------------------
        # ISSUES
        # ------------------------------------------

        if validation["issues"]:

            st.subheader(
                "⚠️ Potential Issues"
            )

            for issue in validation["issues"]:

                st.error(issue)


        # ------------------------------------------
        # RAW OCR
        # ------------------------------------------

        with st.expander(
            "🔎 View Raw OCR Results"
        ):

            for item in all_ocr:

                st.write(
                    f"**{item['text']}**"
                )

                st.caption(
                    f"Confidence: "
                    f"{item['confidence'] * 100:.2f}%"
                )

                st.write(
                    f"Bounding box: "
                    f"{item['box']}"
                )

                st.divider()


        st.success(
            "📚 Scan saved to History."
        )