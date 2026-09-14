import os
import streamlit as st

from scan.scan import scan_product
from ocr import run_ocr, get_average_confidence
from test_parser import parse_product
from validator import validate_product
from history import save_scan, load_history, create_scan_id


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="FMCG Label Compliance Auditor",
    page_icon="📦",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #666;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .result-box {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📦 FMCG Auditor")

page = st.sidebar.radio(
    "Navigation",
    [
        "📷 Scan Product",
        "📚 History"
    ]
)


# =========================================================
# SCAN PRODUCT PAGE
# =========================================================

if page == "📷 Scan Product":

    st.markdown(
        '<div class="main-title">AI-Based FMCG Label Compliance Auditor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Upload the front and back images of a packaged commodity '
        'to analyze its label.'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # IMAGE UPLOAD
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📸 Front Image")

        front_image = st.file_uploader(
            "Upload front side",
            type=["jpg", "jpeg", "png"],
            key="front_image"
        )

        if front_image is not None:
            st.image(
                front_image,
                caption="Front side",
                width="stretch"
            )

    with col2:

        st.subheader("📸 Back Image")

        back_image = st.file_uploader(
            "Upload back side",
            type=["jpg", "jpeg", "png"],
            key="back_image"
        )

        if back_image is not None:
            st.image(
                back_image,
                caption="Back side",
                width="stretch"
            )


    st.divider()


    # -----------------------------------------------------
    # SCAN BUTTON
    # -----------------------------------------------------

    scan_button = st.button(
        "🔍 Scan Product",
        width="stretch"
    )


    if scan_button:

        if front_image is None:

            st.error(
                "Please upload the front image."
            )

        else:

            # -------------------------------------------------
            # STEP 1: IMAGE SCANNING
            # -------------------------------------------------

            with st.spinner("Validating and saving images..."):

                scan_result = scan_product(
                    front_image,
                    back_image
                )


            # -------------------------------------------------
            # CHECK SCAN RESULT
            # -------------------------------------------------

            if scan_result["status"] != "SUCCESS":

                st.error("Image scanning failed.")

                for error in scan_result["errors"]:
                    st.warning(error)

            else:

                st.success(
                    "Images validated and saved successfully."
                )


                # ---------------------------------------------
                # IMAGE METADATA
                # ---------------------------------------------

                with st.expander("🖼️ Image Information"):

                    if scan_result["front_image"]:

                        st.write("### Front Image")

                        st.json(
                            scan_result["metadata"]["front"]
                        )


                    if scan_result["back_image"]:

                        st.write("### Back Image")

                        st.json(
                            scan_result["metadata"]["back"]
                        )


                # -------------------------------------------------
                # STEP 2: OCR
                # -------------------------------------------------

                with st.spinner(
                    "Extracting text from product images..."
                ):

                    front_ocr = run_ocr(
                        scan_result["front_image"]
                    )

                    back_ocr = []

                    if scan_result["back_image"]:

                        back_ocr = run_ocr(
                            scan_result["back_image"]
                        )


                # Combine OCR results

                ocr_results = (
                    front_ocr +
                    back_ocr
                )


                # -------------------------------------------------
                # OCR RESULT
                # -------------------------------------------------

                if not ocr_results:

                    st.warning(
                        "No text was detected from the images."
                    )

                else:

                    st.success(
                        f"{len(ocr_results)} text elements detected."
                    )


                # -------------------------------------------------
                # OCR CONFIDENCE
                # -------------------------------------------------

                average_confidence = (
                    get_average_confidence(
                        ocr_results
                    )
                )


                st.metric(
                    "Average OCR Confidence",
                    f"{average_confidence * 100:.1f}%"
                )


                # -------------------------------------------------
                # STEP 3: PARSER
                # -------------------------------------------------

                with st.spinner(
                    "Extracting product information..."
                ):

                    product_data = parse_product(
                        ocr_results
                    )


                # -------------------------------------------------
                # STEP 4: VALIDATION
                # -------------------------------------------------

                with st.spinner(
                    "Checking extracted information..."
                ):

                    validation_result = validate_product(
                        product_data,
                        ocr_results
                    )


                # -------------------------------------------------
                # RESULT
                # -------------------------------------------------

                st.divider()

                st.subheader("📊 Compliance Result")

                status = validation_result["status"]


                if status == "COMPLIANT":

                    st.success(
                        "✅ COMPLIANT"
                    )

                elif status == "NEEDS REVIEW":

                    st.warning(
                        "⚠️ NEEDS REVIEW"
                    )

                else:

                    st.error(
                        "❌ POTENTIAL VIOLATION"
                    )


                # -------------------------------------------------
                # EXTRACTED DECLARATIONS
                # -------------------------------------------------

                st.subheader(
                    "📋 Extracted Product Information"
                )

                col1, col2 = st.columns(2)


                with col1:

                    st.write(
                        "**MRP:**",
                        product_data.get("mrp")
                    )

                    st.write(
                        "**Net Quantity:**",
                        product_data.get("quantity")
                    )

                    st.write(
                        "**Manufacturer:**",
                        product_data.get("manufacturer")
                    )


                with col2:

                    st.write(
                        "**Importer:**",
                        product_data.get("importer")
                    )

                    st.write(
                        "**Consumer Care:**",
                        product_data.get("consumer_care")
                    )


                # -------------------------------------------------
                # ISSUES
                # -------------------------------------------------

                if validation_result["issues"]:

                    st.subheader(
                        "⚠️ Issues Detected"
                    )

                    for issue in validation_result["issues"]:

                        st.warning(issue)


                # -------------------------------------------------
                # RAW OCR
                # -------------------------------------------------

                with st.expander(
                    "🔎 View Raw OCR Text"
                ):

                    for item in ocr_results:

                        st.write(
                            f"**{item['text']}** "
                            f"(confidence: "
                            f"{item['confidence']:.2f})"
                        )


                # -------------------------------------------------
                # SAVE HISTORY
                # -------------------------------------------------

                scan_id = create_scan_id()


                history_record = {

                    "scan_id": scan_id,

                    "front_image": scan_result[
                        "front_image"
                    ],

                    "back_image": scan_result[
                        "back_image"
                    ],

                    "metadata": scan_result[
                        "metadata"
                    ],

                    "product_data": product_data,

                    "validation": validation_result,

                    "ocr_confidence": average_confidence
                }


                save_scan(
                    history_record
                )


                st.success(
                    "✅ Scan saved to history."
                )


# =========================================================
# HISTORY PAGE
# =========================================================

elif page == "📚 History":

    st.markdown(
        '<div class="main-title">📚 Scan History</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Previously scanned products'
        '</div>',
        unsafe_allow_html=True
    )


    history = load_history()


    if not history:

        st.info(
            "No scanned products yet."
        )

    else:

        st.write(
            f"Total scans: **{len(history)}**"
        )


        # -------------------------------------------------
        # DISPLAY HISTORY
        # -------------------------------------------------

        for index, scan in enumerate(history):

            scan_id = scan.get(
                "scan_id",
                f"Scan {index + 1}"
            )

            validation = scan.get(
                "validation",
                {}
            )

            status = validation.get(
                "status",
                "UNKNOWN"
            )


            with st.expander(
                f"📦 {scan_id} — {status}"
            ):

                # -----------------------------------------
                # IMAGES
                # -----------------------------------------

                col1, col2 = st.columns(2)


                with col1:

                    front_path = scan.get(
                        "front_image"
                    )

                    if (
                        front_path
                        and os.path.exists(front_path)
                    ):

                        st.image(
                            front_path,
                            caption="Front Image",
                            width="stretch"
                        )


                with col2:

                    back_path = scan.get(
                        "back_image"
                    )

                    if (
                        back_path
                        and os.path.exists(back_path)
                    ):

                        st.image(
                            back_path,
                            caption="Back Image",
                            width="stretch"
                        )


                # -----------------------------------------
                # PRODUCT DATA
                # -----------------------------------------

                st.subheader(
                    "Extracted Information"
                )

                product_data = scan.get(
                    "product_data",
                    {}
                )


                st.write(
                    "**MRP:**",
                    product_data.get("mrp")
                )

                st.write(
                    "**Net Quantity:**",
                    product_data.get("quantity")
                )

                st.write(
                    "**Manufacturer:**",
                    product_data.get("manufacturer")
                )

                st.write(
                    "**Importer:**",
                    product_data.get("importer")
                )

                st.write(
                    "**Consumer Care:**",
                    product_data.get("consumer_care")
                )


                # -----------------------------------------
                # ISSUES
                # -----------------------------------------

                issues = validation.get(
                    "issues",
                    []
                )


                if issues:

                    st.subheader(
                        "⚠️ Issues"
                    )

                    for issue in issues:

                        st.warning(issue)