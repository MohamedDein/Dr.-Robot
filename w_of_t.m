T = 0:1:20 ;
w = (2*pi)*(T.^-1) ;
plot (T,w,'b'); 
xlabel ('T');
ylabel ('w');

title ('w function of T');