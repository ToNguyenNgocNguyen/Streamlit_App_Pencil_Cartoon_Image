# import the frameworks, packages and libraries
import streamlit as st
from PIL import Image
from io import BytesIO
import numpy as np
import cv2 # computer vision

# function to convert an image to a
# water color sketch
def convertto_cartoon(inp_img):
	grey_img = cv2.cvtColor(inp_img,cv2.COLOR_RGB2GRAY)
	blur = cv2.medianBlur(grey_img, 5)
	edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 11)
	color = cv2.bilateralFilter(inp_img, 11, 250, 250)
	cartoon = cv2.bitwise_and(color, color, mask=edges)
	return(cartoon)

# function to convert an image to a pencil sketch
def pencilsketch(inp_img):
	grey_img = cv2.cvtColor(inp_img, cv2.COLOR_RGB2GRAY)
	invert = cv2.bitwise_not(grey_img)
	blur = cv2.GaussianBlur(invert, (21, 21), 0)
	invertedblur = cv2.bitwise_not(blur)
	img_pencil_sketch = cv2.divide(grey_img, invertedblur, scale=256.0)
	return(img_pencil_sketch)

# function to load an image
def load_an_image(image):
	img = Image.open(image)
	return img

# the main function which has the code for
# the web application
def main():
	
	# basic heading and titles
	st.title('WEB APPLICATION TO CONVERT IMAGE TO SKETCH')
	st.write("This is an application developed for converting\
	your ***image*** to a ***Cartoon Color Sketch*** OR ***Pencil Sketch***")
	st.subheader("Please Upload your image")
	
	# image file uploader
	image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])

	# if the image is uploaded then execute these
	# lines of code
	if image_file is not None:
		
		# select box (drop down to choose between water
		# color / pencil sketch)
		option = st.selectbox('How would you like to convert the image',
							('Convert to cartoon color sketch',
							'Convert to pencil sketch'))
		if option == 'Convert to cartoon color sketch':
			image = Image.open(image_file)
			final_sketch = convertto_cartoon(np.array(image))
			im_pil = Image.fromarray(final_sketch)

			# two columns to display the original image and the
			# image after applying water color sketching effect
			col1, _, col2 = st.columns(3, gap='large')
			with col1:
				st.header("Original Image")
				st.image(load_an_image(image_file), width=500)

			with col2:
				st.header("Cartoon Sketch")
				st.image(im_pil, width=500)
				buf = BytesIO()
				img = im_pil
				img.save(buf, format="JPEG")
				byte_im = buf.getvalue()
				st.download_button(
					label="Download image",
					data=byte_im,
					file_name="watercolorsketch.png",
					mime="image/png"
				)

		if option == 'Convert to pencil sketch':
			image = Image.open(image_file)
			final_sketch = pencilsketch(np.array(image))
			im_pil = Image.fromarray(final_sketch)
			
			# two columns to display the original image
			# and the image after applying
			# pencil sketching effect
			col1, _, col2 = st.columns(3, gap='large')
			with col1:
				st.header("Original Image")
				st.image(load_an_image(image_file), width=500)

			with col2:
				st.header("Pencil Sketch")
				st.image(im_pil, width=500)
				buf = BytesIO()
				img = im_pil
				img.save(buf, format="JPEG")
				byte_im = buf.getvalue()
				st.download_button(
					label="Download image",
					data=byte_im,
					file_name="watercolorsketch.png",
					mime="image/png"
				)


if __name__ == '__main__':
	main()
