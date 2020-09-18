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
python 3.8 is used for the devellopement, about te packages there is a requirement file (that I will update later with the correct entries because I f*cked up my virtual envirement).

## Examples
  ### Who is in the picture ?
  #### Request
  `POST /api/v0/operation/`

    curl --location --request POST 'http://localhost:8080/api/v0/operation' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "operation_type":"faceInPicture",
        "algo":"face_recognition",
        "references":[
            {"url":"https://i.imgur.com/uaAe4lp.jpg","label":"Obama"},
            {"url":"https://i.imgur.com/bpqwx0B.jpg","label":"Trump"},
            {"url":"https://gmsrp.cachefly.net/images/19/04/05/0bf8d3663b1525197779635c87ee8e16/960.jpg","label":"messi"}
            ],
        "target" : "https://i.imgur.com/9PPtX.jpg"
    }'

  #### Response
  `{"id":"5f64fc6e3031b39ab15a1be4","results":["Obama"]}`

  ### Who is the writer ?
  #### Request
  `POST /api/v0/operation/`

    curl --location --request POST 'http://localhost:8080/api/v0/operation' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "operation_type":"writer",
        "algo":"SDB",
        "references":[
            {"url":"https://i.imgur.com/5t5VggW.jpeg","label":"Hamid"},
            {"url":"https://i.imgur.com/v2ByskF.jpeg","label":"Hamid"},
            {"url":"https://i.imgur.com/sixqaVc.jpeg","label":"Jilali"},
            {"url":"https://i.imgur.com/tlpgYt3.jpeg","label":"Jilali"},
            {"url":"https://i.imgur.com/aZLnxau.jpeg","label":"Hmadi"}
            ],
        "target" : "https://i.imgur.com/vIYpSuG.jpeg"
    }'

  #### Response
  `{"id":"5f64ffcb3031b39ab15a1be5","results":["Hmadi"]}`

  ### What happened in the operation '5f64fc6e3031b39ab15a1be4' ?
  #### Request
  `GET /api/v0/operation/`

    curl --location --request GET 'http://localhost:8080/api/v0/operation?id=5f64fc6e3031b39ab15a1be4'

  #### Response
  ```json
  {
    "operation_type": "faceInPicture",
    "algo": "face_recognition",
    "references": [
        {
            "url": "https://i.imgur.com/uaAe4lp.jpg",
            "label": "Obama"
        },
        {
            "url": "https://i.imgur.com/bpqwx0B.jpg",
            "label": "Trump"
        },
        {
            "url": "https://gmsrp.cachefly.net/images/19/04/05/0bf8d3663b1525197779635c87ee8e16/960.jpg",
            "label": "messi"
        }
    ],
    "target": "https://i.imgur.com/9PPtX.jpg",
    "revised": false,
    "claimedFalse": false,
    "date": "2020-09-18 18:29:02",
    "results": [
        "Obama"
    ],
    "id": "5f64fc6e3031b39ab15a1be4"
  }
  ```
  ### and others ...
  
## Details of the algorithms, references ...
Coming soon ...