#%%writefile app.py
 
import pickle
import streamlit as st
 
    
#Les variables de la fonction prediction sont X = dataset[['Gender',' Married','ApplicantIncome','Loan_Amount_Term','Credit_History']]


#loading the trained model
pickle_in = open('Emerald_Model_tuto.pkl', 'rb') 
classifier = pickle.load(pickle_in)
 
st.cache()
  
# defining the function which will make the prediction using the data which the user inputs 
def prediction(Gender, Married, ApplicantIncome, Loan_Amount_Term, Credit_History):   
 
    # Pre-processing user input    
    if Gender == "Male":
        Gender = 0
    else:
        Gender = 1
 
    if Married == "Unmarried":
        Married = 0
    else:
        Married = 1
 
    if Credit_History == "Unclear Debts":
        Credit_History = 0
    else:
        Credit_History = 1  
 
    Loan_Amount_Term = Loan_Amount_Term/ 1000
 
    # Making predictions 
    prediction = classifier.predict([[Gender, Married, ApplicantIncome, Loan_Amount_Term, Credit_History]])
     
    if prediction == 0:
        pred = 'Rejected'
    else:
        pred = 'Approved'
    return pred
      
  
# this is the main function in which we define our webpage  

def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:purple;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Streamlit Loan Prediction ML App</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # following lines create boxes in which user can enter data required to make prediction 
    Gender = st.selectbox('Gender',("Male","Female"))
    
    Married = st.selectbox('Marital Status',("Unmarried","Married")) 
    
    ApplicantIncome = st.number_input("Applicants monthly income") 
    
    Loan_Amount_Term = st.number_input("Total loan amount")
    
    Credit_History = st.selectbox('Credit_History',("Unclear Debts","No Unclear Debts"))
    
    result =""
      
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        
        result = prediction(Gender, Married, ApplicantIncome, Loan_Amount_Term, Credit_History) 
        
        st.success('Your loan is {}'.format(result))
        
        print(Loan_Amount_Term)
        
     
if __name__=='__main__':
    main()