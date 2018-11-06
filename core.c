
// Hoeffding's famous bound
inline double hoeffding_1(double sox, double tox, int n, double replacement) {
	if (sox<0 || tox<0) {
		printf("ERR1\n");
		return NAN;
	}
	if (tox>=1)
		return replacement;
	double aa = sox+tox;
	double a = sox/aa;
	double bb = 1-tox;
	double b = 1/bb;
	double e = (n*1.0)/(sox+1);
	aa = aa*e;
	bb = bb*e;
	return pow(a,aa)*pow(b,bb);
}

// our variance bound
inline double hoeffding_2(double s, double t, double d, double D, int n, double replacement) {
	double sox = s/(d*d);
	double tox = t/(d*d);
	if (sox<0 || tox<0) {
		printf("ERR1\n");
		return NAN;
	}
	if (sox>1)
		return 0.0;
	if (sox-tox<=0)
		return replacement;
	if (s>d*(D-d))
		return replacement;
	double AA = 1-sox;
	double BB = 1+tox-sox;
	double CC = sox;
	double DD = sox-tox;
	double EE = pow(AA/BB,BB)*pow(CC/DD,DD);
	return pow(EE,n);
}



// compute the variance bound, for variance s, offset y, domain width D, domain offset d, and n samples
double run_f(double s,double y,double D,double d,int n) {
	double ws = ((n-1)*y+s)*1.0/n;
	double min_inner_val2 = 1.0;
	const double tiny = 0.000001;
	double dd = 0;
	if (d>1-d) 
		dd = d*D;
	else
		dd = D*(1-d);
	for (double phi=0.0; phi<=1.0+tiny; phi+=phi_iterator) {
		double v=hoeffding_2(s,(1-phi)*ws,dd,D,n,0.0);
		v += hoeffding_1(s/((D*(1-d))*(D*(1-d))),sqrt(phi*ws)/(D*(1-d)),n,0.0);
		v += hoeffding_1(s/((d*D)*(d*D)),sqrt(phi*ws)/(d*D),n,0.0);
		if (v<min_inner_val2)
			min_inner_val2 = v;
	}
	return min_inner_val2;
}


