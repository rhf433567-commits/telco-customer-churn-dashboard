
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Telco Customer Churn Dashboard",
    page_icon="📊",
    layout="wide"
)

# تحميل البيانات
df = pd.read_csv("telco_clean.csv")

# عنوان لوحة المعلومات
st.title("📊 لوحة تحليل مغادرة عملاء الاتصالات")
st.write("لوحة تفاعلية لتحليل سلوك العملاء والعوامل المرتبطة بمغادرتهم.")

# الشريط الجانبي والفلاتر
st.sidebar.header("تصفية البيانات")

contracts = st.sidebar.multiselect(
    "نوع العقد",
    options=df["Contract"].unique(),
    default=df["Contract"].unique()
)

internet = st.sidebar.multiselect(
    "خدمة الإنترنت",
    options=df["InternetService"].unique(),
    default=df["InternetService"].unique()
)

payment = st.sidebar.multiselect(
    "طريقة الدفع",
    options=df["PaymentMethod"].unique(),
    default=df["PaymentMethod"].unique()
)

tenure = st.sidebar.multiselect(
    "مدة الاشتراك",
    options=df["TenureGroup"].dropna().unique(),
    default=df["TenureGroup"].dropna().unique()
)

# تطبيق الفلاتر
filtered_df = df[
    (df["Contract"].isin(contracts)) &
    (df["InternetService"].isin(internet)) &
    (df["PaymentMethod"].isin(payment)) &
    (df["TenureGroup"].isin(tenure))
]

# المؤشرات الرئيسية
st.subheader("المؤشرات الرئيسية")

total_customers = len(filtered_df)
churned_customers = (filtered_df["Churn"] == "Yes").sum()

churn_rate = (
    churned_customers / total_customers * 100
    if total_customers > 0 else 0
)

average_charges = (
    filtered_df["MonthlyCharges"].mean()
    if total_customers > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("إجمالي العملاء", f"{total_customers:,}")
col2.metric("العملاء المغادرون", f"{churned_customers:,}")
col3.metric("نسبة المغادرة", f"{churn_rate:.2f}%")
col4.metric("متوسط الرسوم الشهرية", f"{average_charges:.2f}")

# الرسومات البيانية
st.subheader("تحليل مغادرة العملاء")

if total_customers > 0:

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("توزيع العملاء حسب حالة المغادرة")
        churn_counts = filtered_df["Churn"].value_counts()
        st.bar_chart(churn_counts)

    with chart_col2:
        st.write("نسبة المغادرة حسب نوع العقد")
        contract_churn = (
            filtered_df.groupby("Contract")["Churn"]
            .apply(lambda x: (x == "Yes").mean() * 100)
        )
        st.bar_chart(contract_churn)

else:
    st.warning("لا توجد بيانات تطابق الفلاتر المحددة.")

# أهم الاكتشافات
st.subheader("أهم 3 اكتشافات")

st.markdown("""
1. بلغت نسبة مغادرة العملاء أصحاب العقود الشهرية **42.71%**،
   مقارنة بـ **2.83%** لأصحاب عقود السنتين.

2. بلغت نسبة مغادرة عملاء خدمة **Fiber optic** حوالي **41.89%**،
   وهي الأعلى بين أنواع خدمات الإنترنت.

3. وصلت نسبة المغادرة لدى العملاء الجدد الذين تقل مدة اشتراكهم
   عن سنة إلى **47.44%**.
""")
   