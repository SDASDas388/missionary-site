"""C++ 知识：函数"""

import streamlit as st


def _part(title: str, body: str) -> None:
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.markdown(body)


def _answers(kind: str, n: int) -> dict[int, int]:
    """从 1 算到 n，供递归图使用。sum 是累加，fact 是连乘。"""
    values = {1: 1}
    for k in range(2, n + 1):
        previous = values[k - 1]
        values[k] = k + previous if kind == "sum" else k * previous
    return values


def _recursion_mermaid(kind: str, n: int) -> str:
    name = "sumTo" if kind == "sum" else "fact"
    op = "+" if kind == "sum" else "*"
    lines = ["flowchart TB"]
    if n == 1:
        lines.append(f'    N1["{name}(1) = 1"]')
        return "\n".join(lines)
    for k in range(n, 1, -1):
        lines.append(f'    N{k}["{name}({k}) = {k} {op} {name}({k - 1})"]')
    lines.append(f'    N1["{name}(1) = 1"]')
    for k in range(n, 1, -1):
        lines.append(f"    N{k} --> N{k - 1}")
    return "\n".join(lines)


def _show_recursion() -> None:
    kind_label = st.radio(
        "两道题用的是同一副骨架，只是合答案的运算不同",
        ["1 加到 n", "阶乘"],
        horizontal=True,
        key="cpp_recur_kind",
    )
    kind = "sum" if kind_label == "1 加到 n" else "fact"
    n = st.slider("选择 n，看问题怎样一层层变小", 1, 5, 3, key="cpp_recur_n")
    name = "sumTo" if kind == "sum" else "fact"
    op_word = "加上" if kind == "sum" else "乘上"
    values = _answers(kind, n)

    rule_small, rule_stop = st.columns(2)
    with rule_small:
        _part(
            "这一层怎么把问题变小",
            f"`{name}(k)` 自己只{op_word} `k`，"
            f"更小的 `{name}(k - 1)` 交给下一次调用。",
        )
    with rule_stop:
        _part(
            "什么时候能够直接回答",
            f"`{name}(1)` 的答案规定为 1。没有这一层，问题会一直变小，调用停不下来。",
        )

    st.markdown("**往下问：每一层都先挂起，等更小的那一层**")
    st.mermaid_chart(
        _recursion_mermaid(kind, n),
        alt=f"{name} 从 {n} 问到 1 的调用链",
    )
    for k in range(n, 0, -1):
        with st.container(border=True):
            if k == 1:
                st.markdown(
                    f"`{name}(1)` 记住的数是 **1**。这是最小的问题，答案就是 **1**，不再往下问。"
                )
            else:
                st.markdown(
                    f"`{name}({k})` 记住的数是 **{k}**。"
                    f"它还缺 `{name}({k - 1})` 的答案，所以先调用更小的一层，自己在这里等。"
                )

    st.markdown("**往上答：最小的一层先回答，上面每一层用自己记住的数把答案合上**")
    for k in range(1, n + 1):
        with st.container(border=True):
            if k == 1:
                st.markdown(f"`{name}(1)` 回答 **1**。")
            else:
                got = values[k - 1]
                st.markdown(
                    f"`{name}({k})` 收到 **{got}**，"
                    f"和自己记住的 **{k}** 合在一起，回答 **{values[k]}**。"
                )
    st.metric(f"{name}({n}) 的最终答案", values[n])


def render() -> None:
    st.markdown(
        """
        函数把一件事单独包起来。调用它的人提供数据，函数做完后把结果交回来。
        这一章顺着这条线看：函数怎么写、怎么调用、调用里面再调用、自己把更小的同一问题交给自己，以及数据是复制进去还是直接改到原来的变量上。
        """
    )

    st.markdown("## 1. 语法形式、形参、返回值")
    st.markdown(
        """
        先看一个完整的函数。它比较两个整数，把较大的那个交回来。
        """
    )
    st.code(
        """
        int maxOf(int a, int b) {
            if (a > b) {
                return a;
            }
            return b;
        }
        """,
        language="c++",
    )

    type_col, name_col, param_col = st.columns(3)
    with type_col:
        _part("返回类型 `int`", "写在函数名前面。它规定调用表达式本身是一个 `int`：谁调用 `maxOf`，谁就得到一个整数。")
    with name_col:
        _part("函数名 `maxOf`", "后面调用时就写这个名字。名字要能看出这件事情，并遵守标识符的起名规则。")
    with param_col:
        _part("形式参数 `int a, int b`", "括号里每个参数都有类型和名字。它们是函数内部的变量，等调用时再接收数据。")

    st.markdown(
        """
        花括号里是函数体。`return` 后面跟的值就是**返回值**，它的类型必须和返回类型一致。
        `return a;` 里的 `a` 是 `int`，和函数名前面的 `int` 对得上。执行到 `return`，函数立刻结束，这个值交回调用处。

        没有参数时括号留空，例如 `int nextId()`。不交回数据时，返回类型写 `void`，`return` 后面不再跟值。
        """
    )

    st.markdown("## 2. 调用形式")
    st.markdown(
        """
        调用就是写下函数名，并在括号里按顺序放上**实际参数**。实参是这次真正用的数据，形参是函数里准备好的接收位置。
        """
    )
    call_left, call_right = st.columns(2)
    with call_left:
        _part(
            "有返回值",
            "`int bigger = maxOf(3, 8);`\n\n"
            "`3` 进入形参 `a`，`8` 进入形参 `b`。函数交回 `8`，这个整数存进 `bigger`。",
        )
    with call_right:
        _part(
            "没有返回值",
            "`printMax(3, 8);`\n\n"
            "同样按顺序把实参交给形参。函数自己把结果打印出来，调用处不接收返回值。",
        )

    st.markdown(
        """
        下面这个算法只做两件事：记住较大的数，再把它交回来。注释按执行顺序写。
        """
    )
    st.code(
        """
        #include <iostream>
        using namespace std;

        // 形参 a、b 是函数内部的两个整数。
        // 返回类型 int 表示：整次调用的结果是一个整数。
        int maxOf(int a, int b) {
            if (a > b) {
                return a; // a 更大，把 a 的值交回调用处，函数到此结束
            }
            return b;     // 否则把 b 的值交回调用处
        }

        int main() {
            int x = 3;
            int y = 8;
            // 调用形式：函数名(实参, 实参)
            // 3 复制给 a，8 复制给 b；调用表达式的值就是返回值 8
            int bigger = maxOf(x, y);
            cout << bigger << endl;
            return 0;
        }
        """,
        language="c++",
    )

    st.markdown(
        """
        再把「从 1 加到 n」收成函数。循环还是上一章的循环，变化只是：`n` 从参数进来，总和用 `return` 出去。
        """
    )
    st.code(
        """
        // total 从 0 开始。
        // i 从 1 走到 n，每走一步就把 i 加进 total。
        // 循环结束时，total 里是 1+2+...+n，把它交回去。
        int sumTo(int n) {
            int total = 0;
            for (int i = 1; i <= n; i++) {
                total = total + i;
            }
            return total;
        }

        // 调用：sumTo(4) 的值是 10，因为 1+2+3+4 = 10
        int answer = sumTo(4);
        """,
        language="c++",
    )
    st.markdown(
        "调用 `sumTo(4)` 时，形参 `n` 得到 `4`。函数里的 `total` 和 `i` 是这次调用自己的变量，调用结束后它们就释放了，留下来的是返回值 `10`。"
    )

    st.markdown("## 3. 嵌套调用")
    st.markdown(
        """
        一个调用的实参，可以又是一次函数调用。里面的调用先做完，它的返回值再交给外面的函数。
        下面要的是「1+2」和「3+4」里较大的那个和。`larger` 需要两个已经算好的整数，所以两个 `add` 必须先返回。
        """
    )
    st.mermaid_chart(
        """
        sequenceDiagram
            participant Main as main
            participant Add as add
            participant Larger as larger
            Main->>Add: add(1, 2)
            Add-->>Main: 3
            Main->>Add: add(3, 4)
            Add-->>Main: 7
            Main->>Larger: larger(3, 7)
            Larger-->>Main: 7
        """,
        alt="先完成两次加法，再把两个和交给 larger",
    )
    st.code(
        """
        int add(int a, int b) {
            return a + b; // 只负责把两个数相加
        }

        int larger(int a, int b) {
            if (a > b) {
                return a;
            }
            return b; // 只负责比较两个已经拿到的数
        }

        int main() {
            // 从内往外看：
            // 1. add(1, 2) 先返回 3
            // 2. add(3, 4) 再返回 7
            // 3. larger 这时才开始，比较 3 和 7，返回 7
            int answer = larger(add(1, 2), add(3, 4));
            return 0;
        }
        """,
        language="c++",
    )
    step1, step2, step3 = st.columns(3)
    with step1:
        _part("第一步", "`add(1, 2)` 结束，得到 `3`。")
    with step2:
        _part("第二步", "`add(3, 4)` 结束，得到 `7`。")
    with step3:
        _part("第三步", "`larger(3, 7)` 比较这两个返回值，得到 `7`。")

    st.markdown("## 4. 递归调用")
    st.markdown(
        """
        递归是嵌套调用的一种特殊情况：函数调用的还是自己，但交给自己的问题必须更小。

        以「1 加到 n」来说，`sumTo(4)` 可以看成 `4 + sumTo(3)`。这一层只加上自己的 `4`，`1+2+3` 是一个更小的同样问题。
        缩到 `sumTo(1)` 时，答案直接规定为 `1`。然后每一层用自己记住的那个数，把下面交上来的答案合上去。

        拖动下面的 `n`。图表示往下问的方向，卡片先写每一层在等谁，再写答案怎样合回来。
        """
    )
    _show_recursion()
    st.markdown(
        """
        同一个 `sumTo`，循环版用一个 `total` 在**一次调用里**把数加完。递归版每次调用只记住一个 `n`，更小的和等下一次调用交回来。两种写法算的是同一件事。
        """
    )
    st.code(
        """
        // 1 加到 n。
        // n == 1：问题已经最小，答案就是 1。
        // n > 1：这一层记住 n，向 sumTo(n - 1) 要更小的和，再把自己的 n 加上。
        int sumTo(int n) {
            if (n == 1) {
                return 1;
            }
            return n + sumTo(n - 1);
        }

        // sumTo(3) 的往返：
        // sumTo(3) 等着 sumTo(2)，自己记住 3
        // sumTo(2) 等着 sumTo(1)，自己记住 2
        // sumTo(1) 直接回答 1
        // sumTo(2) 收到 1，回答 2 + 1 = 3
        // sumTo(3) 收到 3，回答 3 + 3 = 6
        int answer = sumTo(3);
        """,
        language="c++",
    )
    st.markdown("阶乘只是把「加上更小的答案」换成「乘上更小的答案」，停下来的条件仍然是问题缩到 1。")
    st.code(
        """
        // fact(1) = 1
        // fact(n) = n * fact(n - 1)
        // fact(4) = 4 * 3 * 2 * 1 = 24
        int fact(int n) {
            if (n == 1) {
                return 1;
            }
            return n * fact(n - 1);
        }
        """,
        language="c++",
    )

    st.markdown("## 5. 值传递和引用传递")
    st.markdown(
        """
        调用时，实参进入形参有两种常见方式。值传递交给函数一份副本。引用传递让形参直接绑到原来的变量上，函数里的修改会留在调用处。
        """
    )
    by_value, by_ref = st.columns(2)
    with by_value:
        _part(
            "值传递 `int x`",
            "调用 `addOne(num)` 时，`num` 的值复制给 `x`。\n\n"
            "`x = x + 1` 改的是副本。函数返回后，`num` 仍是原来的数。",
        )
    with by_ref:
        _part(
            "引用传递 `int& x`",
            "形参写成 `int& x`，`x` 就是 `num` 的另一个名字。\n\n"
            "`x = x + 1` 改的是 `num` 自己。函数返回后，`num` 已经变了。",
        )
    st.code(
        """
        #include <iostream>
        using namespace std;

        void addOneByValue(int x) {
            x = x + 1; // 改副本
        }

        void addOneByRef(int& x) {
            x = x + 1; // 改调用处的那一个变量
        }

        int main() {
            int num = 1;
            addOneByValue(num);
            cout << num << endl; // 1

            addOneByRef(num);
            cout << num << endl; // 2
            return 0;
        }
        """,
        language="c++",
    )

    st.markdown(
        """
        交换两个变量要用引用。值传递交换的是函数里的两份副本，`main` 里的 `a` 和 `b` 位置不变。
        引用传递里，形参 `x`、`y` 就是 `a`、`b`，交换会留在 `main` 里。引用形参要绑到变量上，调用时写 `a`、`b` 这样的变量。
        """
    )
    st.code(
        """
        void swapRef(int& x, int& y) {
            int temp = x; // 先把 x 当前的值收起来
            x = y;        // x 改成 y 的值
            y = temp;     // y 改成刚才收起来的旧 x
        }

        int main() {
            int a = 3;
            int b = 8;
            swapRef(a, b); // 返回后 a 是 8，b 是 3
            return 0;
        }
        """,
        language="c++",
    )
    before, after = st.columns(2)
    with before:
        _part("调用 `swapRef(a, b)` 之前", "`a = 3`，`b = 8`。")
    with after:
        _part("调用返回之后", "`a = 8`，`b = 3`。两个变量通过引用被互相换过。")

    st.markdown("## 6. 内联函数和 constexpr 函数")
    normal_call, inline_call = st.columns(2)
    with normal_call:
        _part(
            "普通调用",
            "执行到 `square(4)` 时，程序跳进 `square`，算完再跳回调用的下一行。",
        )
    with inline_call:
        _part(
            "内联之后可能变成的样子",
            "编译器可以把这次调用换成函数体，调用处直接变成 `4 * 4`。源码里仍然写成 `square(4)`。",
        )
    st.markdown(
        """
        `inline` 放在返回类型前面，用来标记特别短的函数。它是给编译器的请求，调用形式和普通函数一样。编译器可以采纳，也可以仍旧生成一次真正的调用。
        """
    )
    st.code(
        """
        inline int square(int x) {
            return x * x;
        }

        int area = square(4); // 写法与普通函数相同
        """,
        language="c++",
    )
    compile_time, run_time = st.columns(2)
    with compile_time:
        _part(
            "编译期间就能算",
            "`side` 和 `square(side)` 都是常量。`area` 在程序运行前就可以得到 `16`。",
        )
    with run_time:
        _part(
            "运行期间再算",
            "同一个 `square`，参数来自输入时，仍然等到运行时再算。`constexpr` 同时允许这两种用法。",
        )
    st.code(
        """
        constexpr int square(int x) {
            return x * x;
        }

        constexpr int side = 4;
        constexpr int area = square(side); // 常量参数，编译时得到 16

        int n;
        cin >> n;
        int runtimeArea = square(n);       // 参数要等输入，运行时再算
        """,
        language="c++",
    )

    st.markdown("## 7. 带默认形参值的函数")
    st.markdown(
        """
        形参可以在声明里带一个默认值。调用时如果省略这个实参，就使用默认值；如果写了实参，就用写上的那个。
        默认值从右往左连续出现：某个参数有默认值时，它右边的参数也都要有默认值。
        """
    )
    default_call, given_call = st.columns(2)
    with default_call:
        _part("`power(3)`", "指数没有写。声明里的默认值把调用补成 `power(3, 2)`，结果是 `9`。")
    with given_call:
        _part("`power(3, 4)`", "指数写了 `4`。默认值不参与这次调用，结果是 `81`。")
    st.code(
        """
        // 默认值写在声明里，调用这个函数的人能看见。
        // exp 在最右边，可以单独带默认值。
        int power(int base, int exp = 2);

        // 定义写出算法：result 从 1 开始，乘上 base，一共乘 exp 次。
        // 这里不再写 = 2，避免和声明里的默认值重复。
        int power(int base, int exp) {
            int result = 1;
            for (int i = 0; i < exp; i++) {
                result = result * base;
            }
            return result;
        }

        int square3 = power(3);    // exp 使用 2，3 * 3 = 9
        int cube3 = power(3, 3);   // exp 使用 3，3 * 3 * 3 = 27
        """,
        language="c++",
    )

    st.markdown("## 8. 函数重载")
    st.markdown(
        """
        同一个名字可以对应多个函数，只要它们的参数个数或参数类型不同。调用时，编译器看实参的个数和类型，选出匹配的那一个。
        只改返回类型、参数列表完全相同，不能构成重载。
        """
    )
    st.mermaid_chart(
        """
        flowchart TD
            OneArg["area(4) 一个整数"] --> Square["area(int side) 边长乘边长"]
            TwoArg["area(3, 5) 两个整数"] --> Rect["area(int width, int height) 宽乘高"]
        """,
        alt="同一个 area，按实参个数进入不同的函数",
    )
    st.code(
        """
        // 一个整数：按正方形计算
        int area(int side) {
            return side * side;
        }

        // 两个整数：按长方形计算
        // 名字仍是 area，参数列表和上面不同，所以是重载
        int area(int width, int height) {
            return width * height;
        }

        int main() {
            int square = area(4);    // 选中 area(int)，4 * 4 = 16
            int rectangle = area(3, 5); // 选中 area(int, int)，3 * 5 = 15
            return 0;
        }
        """,
        language="c++",
    )
    st.markdown(
        "默认形参和重载不要叠在同一个名字上。如果同时存在 `area(int side)` 和 `area(int width, int height = 1)`，调用 `area(4)` 时两个都能配上，编译器无法选择。"
    )

    st.markdown(
        ''':red[missionary--2026.11.09]''',text_alignment="right"
    )
