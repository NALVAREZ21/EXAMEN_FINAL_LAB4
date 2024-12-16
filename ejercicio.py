import streamlit as st;
import pandas as pd;
import numpy as np;
import matplotlib.pyplot as plt;

st.set_page_config(page_title="Ventas por Sucursal");

def detalles():
    st.markdown('**Legajo:** 58731');
    st.markdown('**Comisión:** C2');
    st.markdown('**Nombre:** Alvarez Nicolas');


def crear_grafico(datos_producto, producto):
    ventas_por_producto = datos_producto.groupby(['Año', 'Mes'])['Unidades_vendidas'].sum().reset_index();
    fig, gr = plt.subplots(figsize=(10, 6));
    gr.plot(range(len(ventas_por_producto)), ventas_por_producto['Unidades_vendidas'], label=producto);

    x = np.arange(len(ventas_por_producto));
    y = ventas_por_producto['Unidades_vendidas'];
    z = np.polyfit(x, y, 1);
    tendencia = np.poly1d(z);

    gr.plot(x, tendencia(x), linestyle='--', color='red', label='Tendencia');
    gr.set_title('Evolución de Ventas Mensual', fontsize=16);
    gr.set_xlabel('Año-Mes');
    gr.set_xticks(range(len(ventas_por_producto)));

    etiquetas = [f"{row.Año}" if row.Mes == 1 else "" for row in ventas_por_producto.itertuples()];
    gr.set_xticklabels(etiquetas);
    gr.set_ylabel('Unidades Vendidas');
    gr.set_ylim(0, None);
    gr.legend(title='Producto');
    gr.grid(True);

    return fig;

st.sidebar.header("Suba los archivos");
archivo_cargado = st.sidebar.file_uploader("Suba el archivo (.csv)", type=["csv", "docx"]);

if archivo_cargado is not None:
    if archivo_cargado.name.lower().endswith(".csv"):
        st.success("El archivo tiene una extensión válida");
        datos = pd.read_csv(archivo_cargado);

        sucursales = ["Todas"] + datos['Sucursal'].unique().tolist();
        sucursal_seleccionada = st.sidebar.selectbox("Seleccionar Sucursal", sucursales);

        if sucursal_seleccionada == "Todas":
            st.title("Datos de Ventas Totales");
        else:
            datos = datos[datos['Sucursal'] == sucursal_seleccionada];
            st.title(f"Datos de Ventas en {sucursal_seleccionada}");

        productos = datos['Producto'].unique();

        for producto in productos:
            st.subheader(f"{producto}");
            datos_producto = datos[datos['Producto'] == producto];

            datos_producto['Precio_promedio'] = np.where(
                datos_producto['Unidades_vendidas'] > 0,
                datos_producto['Ingreso_total'] / datos_producto['Unidades_vendidas'],
                0
            )
            precio_promedio = datos_producto['Precio_promedio'].mean();

            datos_producto['Ganancia'] = datos_producto['Ingreso_total'] - datos_producto['Costo_total'];
            datos_producto['Margen'] = np.where(
                datos_producto['Ingreso_total'] > 0,
                (datos_producto['Ganancia'] / datos_producto['Ingreso_total']) * 100,
                0
            )
            margen_promedio = datos_producto['Margen'].mean();
            unidades_vendidas = datos_producto['Unidades_vendidas'].sum();

            col1, col2 = st.columns([1, 2]);

            with col1:
                st.metric(label="Precio Promedio", value=f"${precio_promedio:,.2f}".replace(",", "."));
                st.metric(label="Margen Promedio", value=f"{margen_promedio:.2f}%".replace(",", "."));
                st.metric(label="Unidades Vendidas", value=f"{unidades_vendidas:,}".replace(",", "."));

            with col2:
                fig = crear_grafico(datos_producto, producto);
                st.pyplot(fig);
    else:
        st.error("Archivo erroneo!!! Solo archivo con extension .csv");
detalles()
