import flask
import joblib
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler

#with open('models/randomforest.pkl', 'rb') as f:
 #    clf = joblib.load(f)

#with open('models/logistic.pickel', 'rb') as f:
#   clf = joblib.load(f)

# Read accuracy from file
accuracy_values = {}
with open('accuracy.txt', 'r') as f:
    for line in f:
        key, value = line.strip().split('=')
        accuracy_values[key] = float(value)
      

genders_to_int = {'MALE':1,
                  'FEMALE':0}

married_to_int = {'YES':1,
                  'NO':0}

education_to_int = {'GRADUATED':1,
                  'NOT GRADUATED':0}

dependents_to_int = {'0':0,
                      '1':1,
                      '2':2,
                      '3+':3}

self_employment_to_int = {'YES':1,
                          'NO':0}                      

property_area_to_int = {'RURAL':0,
                        'SEMIRURAL':1, 
                        'URBAN':2}




app = flask.Flask(__name__, template_folder='templates')
@app.route('/')
def main():
    return (flask.render_template('index.html'))

@app.route('/report')
def report():
    return (flask.render_template('report.html'))



@app.route("/Loan_Application", methods=['GET', 'POST'])
def Loan_Application():
    
    if flask.request.method == 'GET':
        return (flask.render_template('Loan_Application.html'))
    
    if flask.request.method =='POST':
        
        #get input
        #gender as string
        genders_type = flask.request.form['genders_type']
        #marriage status as boolean YES: 1 , NO: 0
        marital_status = flask.request.form['marital_status']
        #Dependents: No. of people dependent on the applicant (0,1,2,3+)
        dependents = flask.request.form['dependents']
        
        #education status as boolean Graduated, Not graduated.
        education_status = flask.request.form['education_status']
        #Self_Employed: If the applicant is self-employed or not (Yes, No)
        self_employment = flask.request.form['self_employment']
        #Applicant Income
        applicantIncome = float(flask.request.form['applicantIncome'])
        #Co-Applicant Income
        coapplicantIncome = float(flask.request.form['coapplicantIncome'])
        #loan amount as integer
        loan_amnt = float(flask.request.form['loan_amnt'])
        #term as integer: from 10 to 365 days...
        term_d = int(flask.request.form['term_d'])
        # credit_history
        credit_history = int(flask.request.form['credit_history'])
        
        property_area = flask.request.form['property_area']
        
        valuation = int(flask.request.form['valuation'])

        selected_model=flask.request.form['model_selection']


        #create original output dict
        output_dict= dict()
        output_dict['Applicant Income'] = applicantIncome
        output_dict['Co-Applicant Income'] = coapplicantIncome
        output_dict['Loan Amount'] = loan_amnt
        output_dict['Loan Amount Term']=term_d
        output_dict['Credit History'] = credit_history
        output_dict['Gender'] = genders_type
        output_dict['Marital Status'] = marital_status
        output_dict['Education Level'] = education_status
        output_dict['No of Dependents'] = dependents
        output_dict['Self Employment'] = self_employment
        output_dict['Property Area'] = property_area
        output_dict['Property Valuation'] = valuation


        x = np.zeros(21)
    
        x[0] = applicantIncome
        x[1] = coapplicantIncome
        x[2] = loan_amnt
        x[3] = term_d
        x[4] = credit_history

        print('------this is array data to predict-------')
        print('X = '+str(x))
        print('------------------------------------------')

        if(selected_model=='randomforest'):
            clf = joblib.load(open("models/randomforest.pkl", "rb")) 
           
        elif(selected_model == 'logistic'):
            clf = joblib.load(open("models/logistic.pickle", "rb")) 
            

        pred = clf.predict([x])[0]
        
        if pred == 1:
            if (selected_model=='randomforest'):
                res = f'🎊🎊Congratulations!!! You are eligible to take a loan!!!🎊🎊 Accuracy: {accuracy_values["clf_rf_accuracy"] * 100:.2f}% using ramdom forest 🎉'
            elif(selected_model == 'logistic'):
                res = f'🎊🎊Congratulations!!! You are eligible to take a loan!!!🎊🎊 Accuracy: {accuracy_values["clf_lr_accuracy"] * 100:.2f}% using logistic regression🎉'
            decline_reasons = None
        
        else:  # If the loan is declined
            
            res = '😔😔SORRY!!! You are not eligible!!!😔😔'
            decline_reasons = {}    
            if applicantIncome < 3000:
                decline_reasons['Income'] = 'Insufficient income'
            if credit_history < 1:
                decline_reasons['Credit History'] = 'Poor credit history'
            if valuation < 10000:
                decline_reasons['Valuation'] = 'Your property isnt worth much'
            
        #render form again and add prediction
        return flask.render_template('Loan_Application.html', 
                                     original_input=output_dict,
                                     result=res,decline_reasons=decline_reasons)
      
if __name__ == '__main__':
    app.run(debug=True) 