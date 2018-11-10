from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from clarifai.rest import ClarifaiApp, Concept

app = ClarifaiApp(api_key='d4d5faab185e4590b14866212e252f3b')

model = app.models.get('general-v1.3')

select_concept_list = [Concept(concept_name='car')]
print(model.predict_by_url(url='https://s.driving-tests.org/wp-content/uploads/2012/02/back-parking.jpg', select_concepts=select_concept_list))
