# DroneStitch
#### Video Demo: https://www.youtube.com/watch?v=VzK3LAmHUl0
## Description:
This porject is part of Harvards CS50's Introduction to Computer Science. This final project is a web application designed for drone operators to upload multiple topdown site survey photos to be stitched togther to make larger panoramic picture.

The key factors to consider when usding this application are:
- Number of Photos
    - The number of photos that you upload will drematically increase the amount of time that it will take for the stitching alorithim to create an output image.
- Number of unique identifiers
    - The more uniqure identifiers that are present across multiple pictures the easier it is for the stitching alorithim to create an acreate image. If there are not enough unique identifiers there is a possablility that the stitching alorithim will be unale to stich the multiple photos together.
- Overlap of photos
    - The ideal overlap for the pictures is 40%. This enable the stitching alorithm it identify multiple commonalities and unique identifiers between the images to stitch them together. The loss overlap that you have on you images the more promanate your unique identifiers must be.

### Implomentation:
To achive this I reasearched what the best implomentation for such a meathod like this would be and I decided to use OpenCV's libary of computer visision tools.

This is due to the image processing techniques that they utilise, such as keypoint detection, local invariant dscriports, keypoint matching, and prespective wraping.

#### imageStitching.py
Taking insporation from Adrian Rosebrocks ["Image Stitching with OpenCV and Python"](https://pyimagesearch.com/2018/12/17/image-stitching-with-opencv-and-python/) totorial I was able to imploment an image stitching algorithm using OpenCV. 

This file contains one the main function of the project <code>image_stitch()</code>. This function takes the arguments of wether the user would like to crop the image, the location of the pictures that the user would like to stitch together, and the location that the stitched output should be stored.

<code>image_stitch()</code> First loops through each of the files located at the <code>upload_file</code> location and passess it into <code>cv.imread()</code>. If <code>NULL</code> is returned then the function returns false, else the image is appended to the image list.

The function then desides which version of <code>.stitch()</code> should be used depending on whether OpenCV 3 or 4 is being used. The list of <code>images</code> is then passed into <code>.stitch()</code> and return the status of whether the stitching of the images was successful and the stitched image.

If the status returns <code>0</code> then the function will <code>return False</code>, otherwise the function will see whether the user required the image to be cropped or not. If the user has requested the image to be corped then a 10 pixel black borde is added to all sides of the stiched image. The stitched image is then passed to <code>.cvtColor()</code> to create a grayscale version of the image that is then passed into <code>.threshold()</code> to get a binary image of the stitched image is white and the background are black. This threshold image is then used to get the bounding box of the larger contour. A bounding box of the smallest rectangualr regsion that the entire stitched photo can fit in is generated through callculating a bounding box the largest contor and drawing a solid white rectangle onto a mask. We then reduce the mask size until only forground elements are being displayed. This rectangle is then overalyed onto the rectangle onto <code>stitched</code> image and extract the ROI.

The stitched image is then saved to the output file and a status code is sent to <code>main.py</code>.

### main.py
The flask app has two functions:
#### <code>allowed_files(filename)</code>
This function checks the file name against the <code>ALLOWED_EXTENSIONS</code>, in this case png, jpg or jpeg.

#### <code>index()</code>
This is the main function of the <code>main.py</code>. If index is accessed via <code>'GET',</code> then all files held within the <code>'OUTPUT_FOLDER'</code> will be removed and <code>index.html</code> will be rendered for the user. The user is then able to upload the multiple images that they would like to stitch together, check wether they would like to have the output image croped or not and then upload the files. The main content of the <code>index.html</code> is then hidden and a loading GIF is made visable to indicate to the user that the stitching process is underway. If the user has entered <code>index()</code> via <code>'POST'</code> then we check to see if files where added to the form, if not then they will be redirected to index via <code>'GET'</code> and give a flash message stating there where 'No file part'. A check is then made to see if the files that where uploaded are the apart of the <code>allowed_files()</code>, If the files are then they will be saved to the <code>'UPLOAD_FOLDER'</code> location, else the user will be redirected to index via <code>'GET'</code> and a flash message stating 'Unaccepted file type [file type] uploaded. Approved file types are png, jpg, jpeg.' The images are then passed to <code>image_stitch()</code>. The once the image has been stitched the files within the <code>'UPLOAD_FILE'</code> are removed. If <code>image_stitch()</code> failed then th user will be redirected to index via <code>'GET'</code> and give a flash message stating 'Unable to stitch'. If <code>image_stitch()</code> was successful then <code>success.html</code> will be rendered with the stiched image.
