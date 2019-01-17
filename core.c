
const double tiny = 0.000001;

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
	if (s>d*(D-d)+tiny)
		return replacement;
	double AA = 1-sox;
	double BB = 1+tox-sox;
	double CC = sox;
	double DD = sox-tox;
	double EE = pow(AA/BB,BB)*pow(CC/DD,DD);
	return pow(EE,n);
}

// Maurer and Pontil's entropy variance bound
double entropy(double s, double t, double D, int n) {
	if ((s>D/4.0) || (s<0))
		return 0.0;
	if (t<0)
		return 1.0;
	if ((t>1) || (t>s))
		return 0.0;
	if (s==0)
		return 1.0;
	return exp((-(n-1)*t*t)/(2*s*D*D));
}




// compute the variance bound, for variance s, offset y, domain width D, domain offset d, and n samples
double run_f(double s,double y,double D,double d,int n) {
	if (s>D*D*d*(1-d)) {
		printf("ERR2\n");
		return -1;
	}
	if (y>s) {
		printf("ERR3\n");
		return -1;
	}
	double ws = ((n-1)*y+s)*1.0/n;
	double min_inner_val2 = 1.0;
	double dd = 0;
	if (d>1-d) {
		dd = d*D;
	} else {
		dd = D*(1-d);
	}
	for (double phi=0.0; phi<=1.0+tiny; phi+=phi_iterator) {
		double v=hoeffding_2(s,(1-phi)*ws,dd,D,n,0.0);
		v += hoeffding_1(s/((D*(1-d))*(D*(1-d))),sqrt(phi*ws)/(D*(1-d)),n,0.0);
		v += hoeffding_1(s/((d*D)*(d*D)),sqrt(phi*ws)/(d*D),n,0.0);
		if (v<min_inner_val2)
			min_inner_val2 = v;
	}
	double entropy_val = entropy(s,y,D,n);
	if (min_inner_val2 < entropy_val) {
		return min_inner_val2;
	} else {
		return entropy_val;
	}
}

// compute the inversive function z-1 for parameters a,b,d,D
// where if run_f(s,y,D,d,n) = v then run_g(s-y,v,D,d,n) = s
double run_g(double a, double b, double D, double d, int n) {
	double maxs = D*D*d*(1-d);
	double maxy = maxs-a;
	if ((b>1) || (maxy<0)) {
		printf("ERR4\n");
		return -1;
	}
	if (b<run_f(maxs,maxy,D,d,n)) {
		return -1;
	}
	int p = 1;
	double pval=0;
	double newpval, y, f_val;
	while (p < 20) {
		newpval = pval + 2.0/(2<<p);
		y = maxy*newpval;
		f_val = run_f(a+y,y,D,d,n);
		if (f_val-b>0) {
			pval = newpval;
		}
		p++;
	}
	return a+maxy*pval;
}


