"""Streamlit UI for ML Paper Recommender."""

import os
import sys
from pathlib import Path

import requests
import streamlit as st

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# API base URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="ML Paper Recommender",
        page_icon="📚",
        layout="wide",
    )

    st.title("📚 ML Paper Recommender")
    st.markdown(
        "Upload research papers and discover similar papers with AI-powered explanations."
    )

    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio("Choose a page", ["Upload Paper", "Search Papers", "Browse Papers"])

    if page == "Upload Paper":
        show_upload_page()
    elif page == "Search Papers":
        show_search_page()
    elif page == "Browse Papers":
        show_browse_page()


def show_upload_page():
    """Show the paper upload page."""
    st.header("Upload a Research Paper")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload a research paper in PDF format",
    )

    title_override = st.text_input(
        "Paper Title (optional)",
        help="If left empty, the title will be extracted from the PDF",
    )

    if st.button("Upload and Process", type="primary"):
        if uploaded_file is None:
            st.error("Please upload a PDF file")
            return

        with st.spinner("Processing paper... This may take a minute."):
            try:
                # Prepare file for upload
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                params = {}
                if title_override:
                    params["title"] = title_override

                # Upload to API
                response = requests.post(
                    f"{API_BASE_URL}/upload_pdf",
                    files=files,
                    params=params,
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Paper uploaded and processed successfully!")

                    # Display results
                    st.subheader("Paper Summary")
                    st.write(f"**Title:** {data['title']}")
                    st.write(f"**Paper ID:** `{data['paper_id']}`")

                    st.subheader("Summary")
                    st.write(data["summary"])

                    st.subheader("Keywords")
                    keywords = data.get("keywords", [])
                    if keywords:
                        st.write(", ".join(keywords))

                    st.subheader("Content Snippet")
                    st.write(data["content_snippet"])

                else:
                    error_msg = response.json().get("detail", "Unknown error")
                    st.error(f"❌ Error: {error_msg}")

            except Exception as e:
                st.error(f"❌ Error uploading paper: {str(e)}")


def show_search_page():
    """Show the search page."""
    st.header("Search for Similar Papers")

    query = st.text_input(
        "Enter your search query",
        placeholder='e.g., "papers similar to SAM" or "contrastive learning"',
        help="Describe what kind of papers you're looking for",
    )

    top_k = st.slider("Number of results", min_value=1, max_value=20, value=5)

    if st.button("Search", type="primary"):
        if not query or not query.strip():
            st.error("Please enter a search query")
            return

        with st.spinner("Searching papers and generating explanations..."):
            try:
                response = requests.get(
                    f"{API_BASE_URL}/search",
                    params={"query": query, "top_k": top_k},
                )

                if response.status_code == 200:
                    data = response.json()
                    papers = data.get("papers", [])
                    explanations = data.get("explanations", [])

                    if not papers:
                        st.info("No papers found matching your query.")
                        return

                    st.success(f"Found {len(papers)} similar papers")

                    # Display results
                    for i, (paper, explanation) in enumerate(zip(papers, explanations), 1):
                        with st.expander(
                            f"📄 {i}. {paper['title']} (Similarity: {paper['similarity_score']:.2%})",
                            expanded=(i == 1),
                        ):
                            st.write(f"**Paper ID:** `{paper['id']}`")

                            st.write("**Why this paper is relevant:**")
                            st.info(explanation)

                            st.write("**Summary:**")
                            st.write(paper["summary"])

                            if paper.get("keywords"):
                                st.write("**Keywords:**")
                                st.write(", ".join(paper["keywords"]))

                            st.write("**Content Snippet:**")
                            st.write(paper["content_snippet"])

                else:
                    error_msg = response.json().get("detail", "Unknown error")
                    st.error(f"❌ Error: {error_msg}")

            except Exception as e:
                st.error(f"❌ Error searching: {str(e)}")


def show_browse_page():
    """Show the browse all papers page."""
    st.header("Browse All Papers")

    if st.button("Refresh", type="primary"):
        st.rerun()

    try:
        response = requests.get(f"{API_BASE_URL}/papers")

        if response.status_code == 200:
            data = response.json()
            papers = data.get("papers", [])
            count = data.get("count", 0)

            st.info(f"Total papers in database: {count}")

            if not papers:
                st.info("No papers in database yet. Upload some papers to get started!")
                return

            # Display papers
            for paper in papers:
                metadata = paper.get("metadata", {})
                title = metadata.get("title", "Unknown")
                summary = metadata.get("summary", "")

                with st.expander(f"📄 {title}"):
                    st.write(f"**Paper ID:** `{paper['id']}`")
                    if summary:
                        st.write("**Summary:**")
                        st.write(summary)

                    keywords = metadata.get("keywords", "")
                    if keywords:
                        st.write("**Keywords:**")
                        st.write(keywords.replace(",", ", "))

        else:
            error_msg = response.json().get("detail", "Unknown error")
            st.error(f"❌ Error: {error_msg}")

    except Exception as e:
        st.error(f"❌ Error browsing papers: {str(e)}")


if __name__ == "__main__":
    main()

