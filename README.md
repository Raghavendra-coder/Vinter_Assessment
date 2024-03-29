Constructing a Health and Prosperity Index for US States

**part - 2 : How to run the project**
1. Clone the project in your local using git clone https://github.com/Raghavendra-coder/Vinter_Assessment.git
2. Start your docker server.
3. Open your terminal in the path where "manage.py" file is located. (manage.py is just inside Vinter_Assessment, Vinter_Assessment --> manage.py)
4. So if you are in Vinter_Assessment directory then you are ok else cheange directory to Vinter_Assessment.
5. run docker-compose up --build in the terminal.(with docker server already runnnig)
6. When the nuild will be completed (you will see )
7. After that open 0.0.0.0:8502(the port used by main streamlit).
8. If the data is not updated , you will see it getting updated and if it is already updated you will se the health-prosperity-index with respect to every year.



**What is done in this project**
1. Used the api endpoints to get the required data from datausa.io. (**part-2 point 1 covered here**)
2. From all the data , refined and taken the needed data only. (using pandas and numpy)
3. Updating the final data in database.
4. Fetching the data from database and calculating the health prosperity index. (**part-2 point 2 covered here**)
5. An asynchronous task has been set up that will update the data in database in every 24 hour at 00:00 utc time. This ensures that you pick up any changes that data 
USA may make in their datasets. (**part-2 point 3 covered here**)
6. Showing the result chart using streamlit. (**part-2 point 4 covered here**)
7. Asynchronous task has been setup using celery, celery beats and redis.
8. And finally everything is dockerized.



**Technologies used in this project**
1. python
2. Database Designing
3. Docker
4. Github
5. Bash
6. Django
7. Streamlight
8. SQL (ORMs)


**Part - 1**
1. The variables selected for the Health and Prosperity Index are:

  i) Employment Total Population
  ii) Working Population Total
  iii) Real Estate Taxes by Mortgage
  iv) Household Income
  v) Severe Housing Problems
  vi) Health Insurance Total
  vii) Child Mortality Rate
  viii) Working Average Wage

2. how did you weigh the variables?
   the variables were weighted equally due to the simplicity of the approach
   and the lack of specific guidance on the relative importance of each variable.
   This meant each variable contributed equally to the final index score. 
   The weights were adjusted to maintain equal contribution from each variable.
   Thus, each variable was assigned a weight of 1/8, ensuring an equal impact on the overall index.

3. Can you briefly describe why you chose these variables?
  i) Employment and Working Population : These variables reflect the economic activity and potential of the population, capturing both the quantity and quality of employment opportunities.
  ii) Working Population Total : Measures the potential workforce size, important for understanding economic vitality and the labor market's capacity to drive growth and innovation.
  iii) Real Estate Taxes by Mortgage and Household Income: These indicate the economic stability and standard of living, with real estate investment reflecting confidence in the economy and household income indicating financial health.
  iv) Household Income : Directly measures economic well-being and standard of living, showing the financial capacity of households to access essential services and participate in economic activities.
  v) Severe Housing Problems : This metric provides insight into the quality of living conditions and economic distress within the population, directly impacting health and well-being.
  vi) Health Insurance Total : The accessibility of healthcare services, as indicated by health insurance coverage, directly affects public health outcomes.
  vii) Child Mortality Rate : A fundamental health indicator that reflects the overall health environment, including access to healthcare and the effectiveness of health policies.
  viii) Working Average Wage : Added to provide a direct measure of economic prosperity, reflecting average earnings and the standard of living among the working population.
