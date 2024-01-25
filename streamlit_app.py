import streamlit as st

st.write("Chem Molecule Calculator")



st.markdown(
    """
    To calculate molecular structure simply enter the molecular weight. 
    It will spit out all possible comginations of (H,C,O)
    """

    )

input = st.number_input("Enter Molecular Formula Here As an Integer")
weight = int(input)
i_max = weight
j_max = weight//12
k_max = weight//16
for i in range(i_max+1):
    st.write("____")
    for j in range(j_max+1):
        for k in range(k_max+1):
              sum = i*1+j*12+k*16
              if sum == weight:
                  st.write(f"({i},{j},{k})")
