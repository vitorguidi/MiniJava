class Factorial {
    public static void main(String[] a) {
        System.out.println(new Fac().ComputeFac(10));
    }
}

class Fac {
    int teste;
    public int ComputeFac(int num) {
        int numxaux;
        int foo;
        if (num < 1)
            numxaux = 1;
        else
            numxaux = num * (this.ComputeFac(num-1))
        return numxaux;
    }
}