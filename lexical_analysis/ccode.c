int main(){
    int a, a2, i;
    float b;
    bool mybool;
    a = 10;
    a2 = 200 + a/10;
    i = 0;
    b = 111.123 - 12.0;
    mybool = false;
    while(i<10){
        if(!(a < a2) and b != 10.1){
            a = (a - a2)*2;
            i = i + 1;
        }
        else{
            if(mybool == false){
                mybool = !mybool;
            }
            i = i/2;
        }
    }
}