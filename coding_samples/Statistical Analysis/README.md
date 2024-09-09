README + WRITEUP
Nassima Bouhenni
Prof. Nandakumar
CS 5304
Assignment 1 Question 2

To run program: Python3 p2.py [Extrasensory Individual Input] [Extrasensory Sensor Input]
Output: all histograms (.png), labelled as aast (actual average screen time) or past (percieved average screen time) and fill in method. Additionally, latitude trace as a .png file.

Question 2
Case 1:
A) They are represented as -1.
B) The histogram is skewed right, as there is a floor of 0 but no ceiling. As such the outliers are also
greater than the rest of the data.
C) The datasets look largely similar (there were not many missing values) though the mean and median fill-ins are less skewed with more point near the center. The random value (chosen randomly each time) occasionally introduces outliers, increasing the skew.
D) The lowest p-values actually are associated with the random number fill in, which surprised me, 
probably because it helps to match with the height and width of the normal distribution as it does
not add more data to the center.

Case 2:
A) The data here seems to be (very barely) skewed left with fewer outliers, presumably because people tend to underestimate
their phone usage and tend to guess easy numbers like 5 hours, rather than 6 or 7.
B) 4 intense users.
C) The p-value is relatively small (0.09) but not enough to reject the null hypothesis (0.05), so the data appears to be inconclusively missing. However, I would argue there is a small correlation
and as such the data is MAR, though the correlation doesn't seem to be statistically significant but may rely on other factors not recorded (that could also be related to missing battery level data).

Case 3:
A) I found these people by doing a similar algorithm as in Case 2, in that I compared location data
with battery usage data using a chi-squared test. I found that the p-value was below 0.05 in many cases. To find the minutes lost due to turning-off of the location service, assuming all cases where low battery and no GPS usage are correlated, take the 4th element in the contingency table where both arrays output 'True'. 
B) The filling in methods seem to be largely equivalent in cases where there are not huge gaps in the data. This data was roughly flat at many points and so all 3 fill in methods gave the same values. Personally, because this data deals with jumps in latitude numbers rather than smooth transitions, I would stay away from linear interpolation as it introduces new numbers that would not normally be in the dataset.

