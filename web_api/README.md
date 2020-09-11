# Web Api for the models develloped and face_recognition
Rest api that can :
- Detect the writer of a document based on the handwriting using other labelled references.
- Detect faces in an image and video based on labelled references.
- Store details of operations in a noSQL DB (mongoDB).
- Provide some basic operations on the stored "operations" (get, update, delete) and give some indicators about the general state of the api.
- There is a private mode (by default) and a public one (where an url is generated to thst the api on the internet with a distante web app)

## Representation

![All resources](./api_architecture.png)

## Accepted methodes
- For writer identification :
  - SDVP : Sift descriptors + VLAD + PCA*
  - SEVP : Sift keypoints + Encoder + VLAD + PCA*
  - SDB : Sift descriptors + BOW

	* *: PCA is not added yet considering it's impact on the accuracy
	* Details are in Model_training folder
- For face recognition, the library : https://github.com/ageitgey/face_recognition is used (thanks for them)

## What to install
python 3.8 is used for the devellopement, about te packages there is a requirement file (that I will update later with the correct entries because I f*cked up my vertual envirement).

## Details of the algorithms, references ...
Coming soon ...