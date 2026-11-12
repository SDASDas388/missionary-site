#include<iostream>
using namespace std;


// 构造函数是
// **类的特殊成员函数**，
// 核心作用是：**在创建类的对象时，自动对对象的成员变量进行初始化**，保证对象一被创建就拥有合法的初始值，避免出现未初始化的 “垃圾值”。


//构造函数有三个部分：声明、实现、调用



// 设置常量
const float PI= 3.1415926;   // π
const float FENCE_PRICE = 35;    // 栅栏的单价
const float CONCRETE_PRICE=20;  // 过道水泥单价

class Circle{

public:
    Circle(float r);      // 构造函数（声明）
                        // 它接收一个`float`类型的参数`r`，作用是接收外部传入的半径值，用来初始化类内部的私有成员`radius`。

    float circumference();      // 计算圆的周长
    float area();           // 计算圆的面积

private:
    float radius;   //圆半径
};

// 类的实现

// 构造函数的实现
// 构造函数初始化数据成员 radius
Circle::Circle(float r){
    radius=r;
}

// 计算圆的周长
float Circle::circumference(){
    return 2*PI*radius;
}

// 计算圆的面积
float Circle::area(){
    return PI*radius*radius;
}


//主函数的实现
int main(){
    float radius;
    cout<<"Enter the radius of the pool:";     //提示用户输入半径
    cin >> radius;


    //构造函数的调用（创建对象时自动执行）
    //构造函数不需要手动写代码调用，**只要创建对象，它就会自动运行**
    Circle pool(radius);            //游泳池边界
    Circle poolRim(radius+3);          //栅栏对象

    // 计算栅栏造价并输出
    float fenceCost=poolRim.circumference() * FENCE_PRICE;
    cout<<"Fencing Cost is $"<<fenceCost<<endl;

    // 计算过道造价并输出
    float concreteCost=(poolRim.area()-pool.area()) * CONCRETE_PRICE;
    cout<<"Concrere Cost is $"<<concreteCost<<endl;

    return 0;
}