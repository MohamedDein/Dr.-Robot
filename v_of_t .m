r = 15 ;
T = 0:1:20 ;
v = (2*pi*r)*(T.^-1) ;
plot (T,v,'b'); 
xlabel ('T');
ylabel ('v');

title ('v function of T');