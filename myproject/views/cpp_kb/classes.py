"""C++ 知识：类"""

import streamlit as st

_PI = 3.1415926
_FENCE_PRICE = 35
_CONCRETE_PRICE = 20

_POOL_STEPS = [
    "读入半径，对象都还没有",
    "创建 pool，构造函数写入半径",
    "创建 poolRim，构造函数写入半径加 3",
    "用 poolRim 的周长计算栅栏造价",
    "用两个圆的面积差计算过道造价",
    "main 结束，后创建的对象先析构",
]


def _part(title: str, body: str) -> None:
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.markdown(body)


def _fence_cost(radius: float) -> float:
    return 2 * _PI * (radius + 3) * _FENCE_PRICE


def _concrete_cost(radius: float) -> float:
    rim = radius + 3
    return (_PI * rim * rim - _PI * radius * radius) * _CONCRETE_PRICE


def _show_characteristics() -> None:
    abstract, inherit, poly = st.columns(3)
    with abstract:
        _part(
            "抽象",
            "从一类事物里抽出当前问题要用的特征，其余细节先放下。"
            "游泳池可以有颜色、水深、水温；算造价时只留下半径，以及由半径得到的周长和面积。"
            "这个结果写成类：数据是半径，操作是求周长和求面积。",
        )
    with inherit:
        _part(
            "继承",
            "新类建立在已有类之上，得到已有类的成员，再增加或改写自己的成员。"
            "`Dog` 继承 `Animal` 之后，狗具有吃这个动作，并另有叫。已有类是基类，新类是派生类。",
        )
    with poly:
        _part(
            "多态",
            "调用的写法相同，实际执行的函数由对象的类型决定。"
            "`say(animal)` 都是调用 `speak()`。绑上狗就打印汪，绑上猫就打印喵。",
        )
    st.markdown(
        """
        封装在前言里已经出现：数据和对数据的操作放进同一个类，并用访问控制决定外面能看见什么。
        这一章的 `private` 半径、`public` 周长和面积，就是封装在类上的写法。
        """
    )
    st.markdown("**继承：狗得到动物已有的成员，再增加自己的成员**")
    st.code(
        """
        class Animal {
        public:
            void eat() { cout << "吃" << endl; }
        protected:
            string name;
        };

        class Dog : public Animal {
        public:
            void bark() { cout << "汪" << endl; }
        };

        Dog dog;
        dog.eat();   // Animal 里的公有成员，Dog 继续能用
        dog.bark();  // Dog 自己增加的成员
        """,
        language="c++",
    )
    st.caption("`class Dog : public Animal` 里的 `public` 表示继承时保持基类原来的访问级别。")

    st.markdown("**多态：同一句 `speak()`，由实际对象决定打印什么**")
    st.mermaid_chart(
        """
        flowchart LR
            DogObj["Dog dog"] --> SayDog["say(dog)"] --> Wang["Dog::speak 打印汪"]
            CatObj["Cat cat"] --> SayCat["say(cat)"] --> Miao["Cat::speak 打印喵"]
        """,
        alt="同一调用形式，狗和猫执行各自的 speak",
    )
    st.code(
        """
        class Animal {
        public:
            virtual void speak() { cout << "..." << endl; }
            virtual ~Animal() = default;
        };

        class Dog : public Animal {
        public:
            void speak() override { cout << "汪" << endl; }
        };

        class Cat : public Animal {
        public:
            void speak() override { cout << "喵" << endl; }
        };

        void say(Animal& animal) {
            animal.speak();
        }

        int main() {
            Dog dog;
            Cat cat;
            say(dog); // 汪
            say(cat); // 喵
            return 0;
        }
        """,
        language="c++",
    )
    st.markdown(
        """
        `virtual` 表示这个函数按对象的实际类型来选。`say` 的参数是 `Animal&`，
        调用时可以绑到 `Dog` 或 `Cat`。`override` 标明派生类改写的是基类那个虚函数。
        基类析构函数也写成虚函数，这样通过基类指针删除派生对象时，派生类自己的清理会执行。
        """
    )


def _show_access() -> None:
    rules = {
        ("类外的 main", "public 的 setTime"): (
            True,
            "`main` 写 `myClock.setTime(8, 30, 0)`。公有成员就是类提供给外部的接口。",
        ),
        ("类外的 main", "private 的 hour"): (
            False,
            "`main` 写 `myClock.hour = 8` 时，编译器拒绝。`hour` 只由类自己的成员函数修改。",
        ),
        ("类外的 main", "protected 的 tick"): (
            False,
            "`tick` 对类外关闭。类外能用的是公有的 `setTime`，走时的细节留在类的继承体系里。",
        ),
        ("Clock 的成员函数", "public 的 setTime"): (
            True,
            "成员函数之间可以互相调用。`run` 里可以直接写 `setTime(...)`。",
        ),
        ("Clock 的成员函数", "private 的 hour"): (
            True,
            "`setTime` 的函数体里写 `hour = h`。私有成员对这个类自己的成员函数开放。",
        ),
        ("Clock 的成员函数", "protected 的 tick"): (
            True,
            "本类的成员函数可以调用 `protected` 成员，和调用私有成员一样直接写名字。",
        ),
        ("派生类的成员函数", "public 的 setTime"): (
            True,
            "公有继承之后，基类的公有成员在派生类里仍然公有，派生类的函数可以调用它。",
        ),
        ("派生类的成员函数", "private 的 hour"): (
            False,
            "私有成员只对基类自己的成员函数开放。派生类要改时间，就调用基类公开的 `setTime`。",
        ),
        ("派生类的成员函数", "protected 的 tick"): (
            True,
            "派生类的成员函数可以访问基类的 `protected` 成员。这是 `protected` 和 `private` 的差别。",
        ),
    }
    with st.container(horizontal=True, vertical_alignment="bottom", gap="medium"):
        caller = st.segmented_control(
            "谁来访问",
            ["类外的 main", "Clock 的成员函数", "派生类的成员函数"],
            default="类外的 main",
            required=True,
            key="cpp_access_caller",
        )
        member = st.segmented_control(
            "访问哪个成员",
            ["public 的 setTime", "private 的 hour", "protected 的 tick"],
            default="public 的 setTime",
            required=True,
            key="cpp_access_member",
        )
    allowed, reason = rules[(caller, member)]
    if allowed:
        st.success(reason, title="可以访问")
    else:
        st.error(reason, title="编译器会拒绝")


def _show_target() -> None:
    radius = st.slider("游泳池半径", 1, 20, 10, key="cpp_target_radius")
    which = st.segmented_control(
        "这次调用的是哪个对象",
        ["pool", "poolRim"],
        default="pool",
        required=True,
        key="cpp_target_which",
    )
    used = radius if which == "pool" else radius + 3
    length = 2 * _PI * used
    pool_card, rim_card = st.columns(2)
    with pool_card:
        _part(
            "pool",
            f"半径 **{radius}**。`pool.circumference()` 里，目的对象是 `pool`，用的是这个半径。",
        )
    with rim_card:
        _part(
            "poolRim",
            f"半径 **{radius + 3}**。`poolRim.circumference()` 里，目的对象是 `poolRim`，用的是这个半径。",
        )
    st.metric(f"{which}.circumference()", f"{length:.2f}")
    st.markdown(
        f"`{which}.circumference()` 执行的是同一个函数体 `return 2 * PI * radius;`。"
        f"这一次 `radius` 是目的对象里的 **{used}**，所以周长是 **{length:.2f}**。"
        "函数体里的 `this` 就指向这个目的对象，`radius` 和 `this->radius` 是同一个成员。"
    )


def _show_pool_walk() -> None:
    radius = st.slider("输入的半径", 1, 20, 10, key="cpp_pool_radius")
    step = st.slider("程序执行到哪一步", 0, 5, 2, key="cpp_pool_step")
    st.markdown(f"**第 {step + 1} 步：{_POOL_STEPS[step]}**")

    pool_alive = step >= 1 and step < 5
    rim_alive = step >= 2 and step < 5
    if step == 5:
        pool_text = "已经析构。它先被创建，所以后被析构。"
        rim_text = "已经析构。它后被创建，所以先被析构。"
    else:
        pool_text = (
            f"已构造，`radius = {radius}`。"
            if pool_alive
            else "还没有这个对象。"
        )
        rim_text = (
            f"已构造，`radius = {radius + 3}`。"
            if rim_alive
            else "还没有这个对象。"
        )
    pool_card, rim_card = st.columns(2)
    with pool_card:
        _part("对象 pool", pool_text)
    with rim_card:
        _part("对象 poolRim", rim_text)

    if step >= 3 and step < 5:
        st.metric("栅栏造价", f"{_fence_cost(radius):.2f}")
    if step >= 4 and step < 5:
        st.metric("过道造价", f"{_concrete_cost(radius):.2f}")
    if step == 5:
        st.markdown(
            "局部对象离开 `main` 时析构。顺序与构造相反：先 `poolRim`，后 `pool`。"
            "这个类没有自己申请的资源，编译器生成的析构函数把对象的生命期结束掉。"
        )


def render() -> None:
    st.markdown(
        """
        类把一类事物的数据和操作写在一起。对象是按照这个类创建出来的具体个体。
        这一章从面向对象的三个基本特点开始，接着看类怎么写、对象怎么用、成员函数调用的是谁、
        对象出生和结束时各自动执行什么，再看到类里面嵌入别的对象、用 UML 把类画出来，以及结构体、联合体和枚举。
        """
    )

    st.markdown("## 1. 面向对象程序设计的基本特点")
    st.markdown(
        """
        三个特点解决的是三件不同的事：抽象决定类里留下什么，继承让新类接上已有的类，多态让同一种调用面对不同对象。
        """
    )
    _show_characteristics()

    st.markdown("## 2. 类和对象")
    st.markdown("### 类的定义")
    st.markdown(
        """
        类的定义从 `class` 和类名开始，花括号里写成员，右花括号后面有分号。
        数据成员描述对象里保存的值，成员函数描述对象能做的操作。
        """
    )
    st.code(
        """
        class Circle {
        public:
            Circle(float r);
            float circumference();
            float area();
        private:
            float radius;
        };
        """,
        language="c++",
    )
    name_col, data_col, fn_col = st.columns(3)
    with name_col:
        _part("类名 `Circle`", "后面创建对象、写成员函数时都用这个名字。类名本身是类型，可以像 `int` 一样用来声明变量。")
    with data_col:
        _part("数据成员 `radius`", "每个对象各有自己的一份。`pool` 的半径和 `poolRim` 的半径是两份存储。")
    with fn_col:
        _part("成员函数", "`circumference` 和 `area` 写在类里，调用时要指明是哪一个对象的周长、哪一个对象的面积。")

    st.markdown("### 类成员的访问控制")
    st.markdown(
        """
        `public`、`protected`、`private` 从写下的位置开始生效，直到下一个访问说明符或类结束。
        `class` 在第一个说明符之前的成员默认是 `private`。
        """
    )
    public_col, protected_col, private_col = st.columns(3)
    with public_col:
        _part("`public`", "类外、本类、派生类都可以访问。外部使用这个类时看到的接口放在这里。")
    with protected_col:
        _part("`protected`", "本类和派生类的成员函数可以访问。类外的普通函数不能访问。")
    with private_col:
        _part("`private`", "只有本类的成员函数可以访问。派生类和类外都不直接碰这些成员。")
    st.code(
        """
        class Clock {
        public:
            void setTime(int h, int m, int s);
        protected:
            void tick();
        private:
            int hour, minute, second;
        };
        """,
        language="c++",
    )
    _show_access()

    st.markdown("### 对象")
    st.markdown(
        """
        对象是类的一个实例。声明对象时写出类名和对象名，需要参数时在对象名后面的括号里传入。
        访问对象的公有成员用点号。对象前面是指针时，用箭头 `->`。
        """
    )
    st.code(
        """
        Circle pool(10);             // 创建一个半径为 10 的对象
        float length = pool.circumference();

        Circle* pointer = &pool;
        float same = pointer->circumference();
        """,
        language="c++",
    )
    st.markdown(
        "`pool` 和 `poolRim` 的类型都是 `Circle`，各自保存自己的 `radius`。对一个对象调用成员函数，用的就是该对象自己的那份数据。"
    )

    st.markdown("## 3. 类的成员函数")
    st.markdown("### 成员函数的实现")
    st.markdown(
        """
        成员函数可以在类内直接写出函数体，也可以在类内只声明，在类外再定义。
        类外定义时，函数名前面写类名和作用域解析运算符 `::`，用来说明这个函数属于哪个类。
        """
    )
    inside, outside = st.columns(2)
    with inside:
        _part(
            "类内定义",
            "函数体写在类的花括号里。这个函数同时是内联成员函数，编译器可以在调用处展开它。",
        )
    with outside:
        _part(
            "类外定义",
            "`Circle::area` 里的 `Circle::` 把这个函数接到类上。类内那一行只保留声明。",
        )
    st.code(
        """
        class Circle {
        public:
            float area() {          // 类内定义
                return 3.1415926f * radius * radius;
            }
            float circumference();  // 类内声明
        private:
            float radius;
        };

        float Circle::circumference() { // 类外定义
            return 2 * 3.1415926f * radius;
        }
        """,
        language="c++",
    )

    st.markdown("### 成员函数调用中的目的对象")
    st.markdown(
        """
        `pool.circumference()` 里，点号前面的 `pool` 是这次调用的目的对象。
        函数体中出现的 `radius`，就是目的对象的 `radius`。同一个函数体，换一个目的对象，用的就是另一份半径。
        """
    )
    _show_target()
    st.code(
        """
        float Circle::circumference() {
            return 2 * PI * this->radius; // this 指向目的对象
        }

        pool.circumference();    // this 指向 pool
        poolRim.circumference(); // this 指向 poolRim
        """,
        language="c++",
    )

    st.markdown("### 带默认形参的成员函数")
    st.markdown(
        """
        默认值写在类内的声明上。类外的定义只重复参数类型和名字，不再写默认值。
        调用时从右边连续省略实参，被省略的参数使用声明里的默认值。这和上一章普通函数的默认形参是同一条规则。
        """
    )
    st.code(
        """
        class Clock {
        public:
            void setTime(int h, int m, int s = 0);
        private:
            int hour, minute, second;
        };

        void Clock::setTime(int h, int m, int s) {
            hour = h;
            minute = m;
            second = s;
        }

        Clock myClock;
        myClock.setTime(8, 30);    // s 使用 0
        myClock.setTime(8, 30, 15); // s 使用 15
        """,
        language="c++",
    )

    st.markdown("### 内联成员函数")
    st.markdown(
        """
        类内定义的成员函数默认是内联的。类外定义时，在返回类型前加上 `inline`，也是提出同样的请求：
        编译器可以把这次调用换成函数体。调用处的写法保持 `pool.area()`。
        内联适合特别短的函数。类放在头文件、函数又在类外定义时，加上 `inline`，多个源文件包含这个头文件才能通过链接。
        """
    )
    st.code(
        """
        class Circle {
        public:
            float area();
        private:
            float radius;
        };

        inline float Circle::area() {
            return 3.1415926f * radius * radius;
        }
        """,
        language="c++",
    )

    st.markdown("## 4. 构造函数和析构函数")
    st.markdown("### 构造函数")
    st.markdown(
        """
        构造函数在对象创建时自动执行，用来给数据成员确定初值。它的名字与类名相同，没有返回类型。
        参数写在创建对象时的括号里。一个类可以有多个构造函数，靠参数的个数和类型区分，这是构造函数的重载。
        """
    )
    st.code(
        """
        class Circle {
        public:
            Circle(float r) { radius = r; }
        private:
            float radius;
        };

        Circle pool(10); // 自动调用 Circle(float)，radius 成为 10
        """,
        language="c++",
    )
    st.markdown(
        """
        成员的初值还可以写在构造函数的初始化列表里，位置在参数列表和函数体之间，以冒号开头。
        `radius(r)` 用参数 `r` 初始化成员 `radius`。函数体开始时，这个成员已经有值。
        """
    )
    st.code(
        """
        Circle(float r) : radius(r) {
        }
        """,
        language="c++",
    )

    st.markdown("### 默认构造函数")
    st.markdown(
        """
        默认构造函数是调用时可以不写实参的构造函数。`Circle()` 是默认构造函数。
        所有参数都有默认值的构造函数，也可以不写实参来调用，它同样是默认构造函数。
        """
    )
    generated, absent = st.columns(2)
    with generated:
        _part(
            "编译器会生成一个",
            "类里一个构造函数都没有声明时，编译器生成无参数的默认构造函数。数据成员按各自类型的规则初始化。",
        )
    with absent:
        _part(
            "自己声明了构造函数之后",
            "只要声明了任意一个构造函数，编译器就不再生成默认构造函数。这时 `Circle pool;` 这种不带参数的创建需要自己再声明一个。",
        )
    st.code(
        """
        class Circle {
        public:
            Circle() : radius(1) {}          // 默认构造函数
            Circle(float r) : radius(r) {}
        private:
            float radius;
        };

        Circle unit;     // 调用 Circle()，半径是 1
        Circle pool(10); // 调用 Circle(float)
        """,
        language="c++",
    )

    st.markdown("### 委托构造函数")
    st.markdown(
        """
        委托构造函数在自己的初始化列表里调用本类的另一个构造函数，把初始化工作交给那一个。
        被调用的构造函数先完整执行，然后才执行委托构造函数自己的函数体。
        初始化列表里一旦委托，就只写这一项。
        """
    )
    st.code(
        """
        class Clock {
        public:
            Clock(int h, int m, int s) : hour(h), minute(m), second(s) {}
            Clock() : Clock(0, 0, 0) {} // 委托给上面那个构造函数
        private:
            int hour, minute, second;
        };

        Clock zero; // 先执行 Clock(0, 0, 0)，三个成员都是 0
        """,
        language="c++",
    )

    st.markdown("### 复制构造函数")
    st.markdown(
        """
        复制构造函数用一个已有对象初始化一个正在创建的新对象。参数是本类的引用，通常写成常量引用 `const Circle&`。
        参数如果按值传递，为了把实参复制进参数，又要调用复制构造函数，这个过程停不下来，所以参数用引用。
        """
    )
    st.code(
        """
        class Circle {
        public:
            Circle(float r) : radius(r) {}
            Circle(const Circle& other) : radius(other.radius) {}
        private:
            float radius;
        };

        Circle pool(10);
        Circle backup(pool); // 用 pool 创建 backup，调用复制构造函数
        Circle same = pool;  // 同样是初始化，调用复制构造函数
        """,
        language="c++",
    )
    copy_init, assign = st.columns(2)
    with copy_init:
        _part(
            "创建时复制",
            "`Circle backup(pool);` 和 `Circle same = pool;` 都是在创建新对象，调用复制构造函数。新对象得到一份相同的半径。",
        )
    with assign:
        _part(
            "两个对象都已存在",
            "`backup = pool;` 发生在两个对象都已经构造完成之后，调用的是赋值运算符。那是另一个函数，名字是 `operator=`。",
        )
    st.markdown(
        "自己没有声明复制构造函数时，编译器生成的版本会把每个成员按它自己的复制方式抄到新对象里。半径这样的数值成员，抄过去的是同一个数，两个对象之后各自独立。"
    )

    st.markdown("### 析构函数")
    st.markdown(
        """
        析构函数在对象的生命期结束时自动执行。名字是波浪号加上类名，没有参数，没有返回类型，一个类只有一个。
        函数体里释放这个对象在构造期间申请的资源。局部对象离开它所在的代码块时析构，后构造的先析构。
        """
    )
    st.code(
        """
        class Trace {
        public:
            Trace(const char* objectName) : name(objectName) {
                cout << name << " 构造" << endl;
            }
            ~Trace() {
                cout << name << " 析构" << endl;
            }
        private:
            const char* name;
        };

        int main() {
            Trace a("a");
            Trace b("b");
            return 0;
        }
        // 输出顺序：
        // a 构造
        // b 构造
        // b 析构
        // a 析构
        """,
        language="c++",
    )

    st.markdown("### 移动构造函数")
    st.markdown(
        """
        移动构造函数用一个即将结束的对象初始化新对象，把资源的所有权转过来，而不是再申请一块相同的资源。
        参数类型是右值引用 `Circle&&`。转走之后，把来源对象的指针置空，它的析构函数就不会释放已经交给新对象的资源。
        """
    )
    copy_way, move_way = st.columns(2)
    with copy_way:
        _part(
            "复制",
            "新对象另外申请内存，再把旧对象里的内容逐字节抄过来。旧对象仍然保留自己的内存。",
        )
    with move_way:
        _part(
            "移动",
            "新对象直接拿过来源对象的指针。来源对象的指针改为空。内存还是原来那一块，所有者换成新对象。",
        )
    st.code(
        """
        class Buffer {
        public:
            Buffer(int n) : size(n), data(new char[n]) {}
            Buffer(Buffer&& other) noexcept : size(other.size), data(other.data) {
                other.size = 0;
                other.data = nullptr;
            }
            ~Buffer() { delete[] data; }
        private:
            int size;
            char* data;
        };
        """,
        language="c++",
    )
    st.markdown(
        """
        `noexcept` 告诉调用者，这个移动过程不抛出异常。标准容器在重新安排元素时，会优先使用带 `noexcept` 的移动构造函数。
        想把一个还有名字的对象当成移动来源，用 `Buffer taken(std::move(source));`。`std::move` 在 `<utility>` 里。
        """
    )

    st.markdown("### default 和 delete")
    st.markdown(
        """
        `= default` 明确要求使用编译器生成的那个版本。`= delete` 禁止这种调用，写出来的调用会在编译时失败。
        对象自己用 `new` 申请了内存、析构时用 `delete` 释放时，复制和移动也要一起写好。只想保留编译器的行为，就写成 `= default`。
        """
    )
    st.code(
        """
        class Clock {
        public:
            Clock() = default;                 // 使用编译器生成的默认构造函数
            Clock(const Clock&) = default;     // 使用编译器生成的复制构造函数
            ~Clock() = default;
        private:
            int hour = 0;
            int minute = 0;
            int second = 0;
        };

        class Buffer {
        public:
            Buffer(int n);
            Buffer(const Buffer&) = delete;    // 禁止复制这块缓冲区
            ~Buffer();
        };
        """,
        language="c++",
    )

    st.markdown("### 程序实例")
    st.markdown(
        """
        下面就是 `circle.cpp`。`pool` 和 `poolRim` 各调用一次 `Circle(float)`，把各自的半径写进各自的对象。
        造价用的是这两个对象的成员函数。拖动下面的步数，可以看到对象从创建、使用到析构的顺序。半径保持 10 时，
        栅栏造价约 2858.85，过道造价约 4335.40，和终端里跑出来的结果一致。
        """
    )
    st.code(
        """
        class Circle {
        public:
            Circle(float r);
            float circumference();
            float area();
        private:
            float radius;
        };

        Circle::Circle(float r) { radius = r; }

        int main() {
            float radius;
            cin >> radius;
            Circle pool(radius);       // 构造 pool
            Circle poolRim(radius + 3); // 构造 poolRim
            float fenceCost = poolRim.circumference() * 35;
            float concreteCost = (poolRim.area() - pool.area()) * 20;
            return 0;                  // 先析构 poolRim，再析构 pool
        }
        """,
        language="c++",
    )
    _show_pool_walk()

    st.markdown("## 5. 类的组合")
    st.markdown("### 组合")
    st.markdown(
        """
        组合是一个类的数据成员本身又是另一个类的对象。`Line` 由两个 `Point` 组成。
        创建 `Line` 时，先构造它里面的成员对象，再执行 `Line` 自己的构造函数体。
        成员对象的构造顺序按照它们在类里声明的顺序，和初始化列表里书写的先后无关。析构时顺序相反：先执行 `Line` 的析构函数体，再按声明的相反顺序析构成员对象。
        """
    )
    st.mermaid_chart(
        """
        classDiagram
            class Point {
                -int x
                -int y
                +Point(int x, int y)
            }
            class Line {
                -Point start
                -Point end
                +Line(int x1, int y1, int x2, int y2)
            }
            Line *-- Point : 包含两个点
        """,
        alt="线段类包含两个点对象",
    )
    st.code(
        """
        class Point {
        public:
            Point(int xValue, int yValue) : x(xValue), y(yValue) {}
        private:
            int x;
            int y;
        };

        class Line {
        public:
            // 初始化列表先写 end，实际仍先构造声明在前的 start
            Line(int x1, int y1, int x2, int y2) : end(x2, y2), start(x1, y1) {}
        private:
            Point start;
            Point end;
        };
        """,
        language="c++",
    )
    st.markdown(
        "创建一条 `Line` 的顺序是：`start` 的构造函数、`end` 的构造函数、`Line` 的函数体。离开作用域时：`Line` 的析构函数体、`end` 的析构函数、`start` 的析构函数。"
    )

    st.markdown("### 前向引用声明")
    st.markdown(
        """
        前向引用声明先告诉编译器某个类的名字存在，暂时不给出这个类的成员。
        看到的是不完整类型。不完整类型可以用来声明指针和引用，因为指针和引用的大小是固定的。
        按值声明一个成员对象、继承这个类、或者计算这个类的大小，都要等到类的完整定义出现。
        """
    )
    st.code(
        """
        class Date; // 前向引用声明

        class Person {
        public:
            void setBirthday(Date* day);
        private:
            Date* birthday; // 指针可以使用不完整类型
            // Date birthday; // 按值包含需要 Date 的完整定义
        };

        class Date {
        public:
            Date(int y, int m, int d);
        private:
            int year, month, day;
        };
        """,
        language="c++",
    )
    pointer_ok, value_waits = st.columns(2)
    with pointer_ok:
        _part(
            "`Date* birthday`",
            "编译器已经知道指针占多少字节，`Person` 的大小可以确定。`Date` 的成员可以等到后面再定义。",
        )
    with value_waits:
        _part(
            "`Date birthday`",
            "`Person` 里面要放进一个完整的 `Date` 对象。编译器需要先看到 `Date` 的全部成员，才知道 `Person` 占多少字节。",
        )

    st.markdown("## 6. UML 图形标识")
    st.markdown("### UML 简介")
    st.markdown(
        """
        UML（统一建模语言）用图形描述面向对象设计。代码写每个成员的类型和函数体，图则把类、类之间的关系放在一张图上。
        这一节使用类图。类图里的一个方框是一个类，方框之间的线表示类与类的关系。
        """
    )

    st.markdown("### UML 类图")
    st.markdown(
        """
        一个类画成上、中、下三格：类名、数据成员、成员函数。成员前面的符号表示访问级别：`+` 是 public，`-` 是 private，`#` 是 protected。
        继承用空心三角指向基类。组合用实心菱形放在整体一侧，表示整体负责它包含的部分。
        """
    )
    symbol_public, symbol_private, symbol_protected = st.columns(3)
    with symbol_public:
        _part("`+` public", "类外可以使用。类图里的 `+circumference()` 对应代码里 `public` 下的函数。")
    with symbol_private:
        _part("`-` private", "只在本类使用。类图里的 `-radius` 对应代码里的私有数据成员。")
    with symbol_protected:
        _part("`#` protected", "本类和派生类使用。动物的名字如果只准备给狗、猫这些派生类用，就标成 `#name`。")
    st.markdown("**`Circle` 的类图，对应 `circle.cpp` 里的定义**")
    st.mermaid_chart(
        """
        classDiagram
            class Circle {
                -float radius
                +Circle(float r)
                +circumference() float
                +area() float
            }
        """,
        alt="Circle 的 UML 类图，含私有半径和公有操作",
    )
    st.markdown("**继承和组合画在同一张关系图里**")
    st.mermaid_chart(
        """
        classDiagram
            Animal <|-- Dog
            Animal <|-- Cat
            Line *-- Point
            class Animal {
                #string name
                +speak()
            }
            class Dog {
                +speak()
            }
            class Cat {
                +speak()
            }
        """,
        alt="空心三角表示继承，实心菱形表示组合",
    )
    st.markdown(
        """
        左边两条线是继承：三角指向 `Animal`，`Dog` 和 `Cat` 是派生类。
        `Line *-- Point` 是组合：菱形在 `Line` 一侧，一条线段包含点。
        """
    )

    st.markdown("## 7. 结构体和联合体")
    st.markdown("### 结构体")
    st.markdown(
        """
        `struct` 和 `class` 都可以包含数据成员和成员函数。二者的差别在默认访问级别：
        `struct` 的成员默认是 `public`，`class` 的成员默认是 `private`。
        只用它来把几项相关数据放在一起时，写成结构体，外部可以直接用点号读写公有成员。
        """
    )
    st.code(
        """
        struct Point {
            int x;
            int y;
        };

        Point p;
        p.x = 3;
        p.y = 4;
        """,
        language="c++",
    )
    struct_col, class_col = st.columns(2)
    with struct_col:
        _part("`struct Point`", "没有写访问说明符。`x` 和 `y` 默认公有，`main` 里可以直接写 `p.x = 3`。")
    with class_col:
        _part("`class Point`", "同样不写访问说明符时，`x` 和 `y` 默认私有。类外要改它们，就提供公有的成员函数。")

    st.markdown("### 联合体")
    st.markdown(
        """
        联合体的全部成员从同一块内存的起始地址摆放，大小按其中最大的成员计算。
        同一时刻有意义的是最近一次写入的那个成员。下面的 `int` 和 `float` 在常见的 64 位 Windows 上都是 4 字节，所以这个联合体是 4 字节。
        成员里如果放有构造函数的类型，例如 `string`，就要自己管理那个成员的生命期。这里的联合体只用整数和浮点数。
        """
    )
    st.code(
        """
        union Number {
            int i;
            float f;
        };

        Number value;
        value.i = 1;    // 这 4 字节按 int 写入
        int n = value.i; // 按 int 读回，得到 1
        """,
        language="c++",
    )
    int_card, float_card, union_card = st.columns(3)
    with int_card:
        _part("`int i`", "单独一个 `int` 占 4 字节。")
    with float_card:
        _part("`float f`", "单独一个 `float` 也占 4 字节，和 `i` 从同一个地址开始。")
    with union_card:
        _part("`union Number`", "整体仍是 4 字节。写入 `i` 之后，这 4 字节的当前含义是那个整数。")

    st.markdown("## 8. 枚举类型 enum")
    st.markdown(
        """
        枚举把一组有名字的整数常量放进一个类型。不指定数值时，第一个枚举项是 0，后面依次加 1。
        也可以给某一项指定整数，它后面没写数值的项在这个数上继续加 1。
        """
    )
    days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    day = st.segmented_control(
        "选一个枚举项",
        days,
        default="MON",
        required=True,
        key="cpp_enum_day",
    )
    st.markdown(
        f"`Weekday` 里 `{day}` 的值是 **{days.index(day)}**。"
        "这个数来自它在枚举列表中的位置：`SUN` 是 0，后面每一项加 1。"
    )
    st.code(
        """
        enum Weekday { SUN, MON, TUE, WED, THU, FRI, SAT };

        Weekday today = MON; // 值是 1
        int index = today;   // 不限定作用域的枚举可以传到 int
        """,
        language="c++",
    )
    st.markdown(
        """
        这种枚举的枚举项进入周围的作用域，所以后面不能再有另一个叫 `MON` 的名字。
        `enum class` 把枚举项留在枚举类型里面，使用时写出类型名。它不会自动变成 `int`，需要数值时用 `static_cast<int>`。
        """
    )
    st.code(
        """
        enum class Color { Red, Green, Blue };

        Color ink = Color::Red;
        int code = static_cast<int>(ink); // 0
        """,
        language="c++",
    )
    plain_enum, scoped_enum = st.columns(2)
    with plain_enum:
        _part(
            "`enum Weekday`",
            "枚举项直接写 `MON`。它可以作为整数使用。同一作用域里，这些名字不能再给别的变量或枚举项。",
        )
    with scoped_enum:
        _part(
            "`enum class Color`",
            "枚举项写成 `Color::Red`。把它交给需要 `int` 的地方时，要显式转换。另一个枚举也可以有自己的 `Red`。",
        )

    st.markdown(
        ''':red[missionary--2026.11.12]''',
        text_alignment="right",
    )
