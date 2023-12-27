import streamlit as st


def sidebar():
    with st.sidebar:

        st.markdown("Paste one of the following questions into the chatbox")
        st.markdown("---")
        st.markdown("# Questions")
        st.markdown(
            "- What is mentioned as the cause for the distance between people last year?\n"
            "- What is described as prevailing over tyranny in the speech?\n"
            "- Which leader is accused of misjudging the global response to their actions?\n"
            "- Which country and its people are commended for their resistance and bravery?\n"
            "- How did President Biden describe the American Rescue Plan?\n"
            "- What were the plans to combat inflation?\n"
            "- What did President Biden propose regarding energy and child care costs in his 2022 State of the Union Address?\n"
        )
        st.markdown("---")