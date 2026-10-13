"""Analiza exportaciones agregadas de BigQuery sin consultar el servicio."""
import hashlib
import json
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1] / 'scripts'))
from estructura import informe

def es(n,d=0):
    return f'{n:,.{d}f}'.replace(',','_').replace('.',',').replace('_','.')

def main():
    raw=ROOT/'data/raw'; out=ROOT/'reports'; tables=out/'tables'; figures=out/'figures'
    tables.mkdir(parents=True,exist_ok=True); figures.mkdir(parents=True,exist_ok=True)
    p=pd.read_csv(raw/'thelook_perfil_tablas.csv',dtype={'valor':'string'})
    d=pd.read_csv(raw/'thelook_distribuciones.csv',keep_default_na=False)
    r=pd.read_csv(raw/'thelook_relaciones.csv',dtype={'valor':'string'})
    if p.duplicated(['tabla','campo','metrica']).any() or r.duplicated(['relacion','metrica']).any() or d.duplicated(['tabla','dimension','valor']).any():
        raise ValueError('Claves de agregados repetidas: revisar exportaciones.')
    def pv(t,c,m):
        v=p.loc[(p.tabla==t)&(p.campo==c)&(p.metrica==m),'valor']
        if len(v)!=1: raise ValueError((t,c,m))
        return v.iloc[0]
    def rv(rel,metric):
        return float(r.loc[(r.relacion==rel)&(r.metrica==metric),'valor'].iloc[0])
    def dist(t,dim):
        z=d.loc[(d.tabla==t)&(d.dimension==dim)].copy()
        z['filas']=pd.to_numeric(z.filas)
        z['importe_observado_finito']=pd.to_numeric(z.importe_observado_finito,errors='coerce')
        return z.sort_values('filas',ascending=False)
    sizes={t:int(pv(t,'*','filas')) for t in sorted(p.tabla.unique())}
    pd.DataFrame([{'tabla':t,'filas':n,'clave_nulos':int(pv(t,'order_id' if t=='orders' else 'id','nulos')),'clave_repeticiones':int(pv(t,'order_id' if t=='orders' else 'id','repeticiones_adicionales_no_nulas'))} for t,n in sizes.items()]).to_csv(tables/'dimensiones.csv',index=False)
    coverage=[]
    for rel in sorted(x for x in r.relacion.unique() if ' -> ' in x):
        den=rv(rel,'fk_no_nulas'); matched=rv(rel,'filas_hijas_con_correspondencia')
        coverage.append(dict(relacion=rel,filas_hijas=int(rv(rel,'filas_hijas')),fk_nulas=int(rv(rel,'fk_nulas')),sin_correspondencia=int(rv(rel,'filas_hijas_sin_correspondencia')),cobertura_no_nulas_pct=matched/den*100 if den else None,padres_duplicados=int(rv(rel,'claves_padre_duplicadas')),max_lineas_por_clave=int(rv(rel,'max_filas_hijas_por_clave')),filas_left_join=int(rv(rel,'filas_estimadas_left_join'))))
    pd.DataFrame(coverage).to_csv(tables/'relaciones.csv',index=False)
    anomalies=p[p.metrica.isin(['secuencia_invertida','posteriores_al_inicio_consulta','entrega_sin_envio','venta_anterior_al_registro'])].copy()
    anomalies['casos']=pd.to_numeric(anomalies.valor)
    anomalies['porcentaje']=anomalies.casos/anomalies.denominador.replace(0,float('nan'))*100
    anomalies[['tabla','campo','metrica','casos','denominador','porcentaje']].to_csv(tables/'alertas_temporales.csv',index=False)
    for t,dim,name in [('orders','status','estados_pedidos'),('order_items','status','estados_lineas'),('order_items','categoria_perfil','categorias'),('orders','pais_perfil','paises'),('events','event_type','eventos')]:
        z=dist(t,dim);z['porcentaje_filas']=z.filas/sizes[t]*100;z.to_csv(tables/f'{name}.csv',index=False)
    monthly=dist('orders','mes_registro_UTC').sort_values('valor');monthly.to_csv(tables/'pedidos_mensuales.csv',index=False)
    statuses=dist('orders','status').set_index('valor');line_status=dist('order_items','status').set_index('valor')
    cats=dist('order_items','categoria_perfil'); countries=dist('orders','pais_perfil')
    top_value=cats.sort_values('importe_observado_finito',ascending=False).iloc[0]
    inventory_rel='order_items.product_id vs inventory_items.product_id'
    m=dict(filas=sizes,importe_lineas=float(pv('order_items','sale_price','suma_finitos')),importe_complete=float(line_status.loc['Complete','importe_observado_finito']),pedidos_complete=int(statuses.loc['Complete','filas']),pedidos_cancelled=int(statuses.loc['Cancelled','filas']),pedidos_returned=int(statuses.loc['Returned','filas']),usuarios_con_pedidos=int(rv('orders.user_id -> users.id','claves_hijas_distintas_no_nulas')),lineas_por_pedido=sizes['order_items']/sizes['orders'],categoria_mas_lineas=str(cats.iloc[0].valor),categoria_mas_lineas_n=int(cats.iloc[0].filas),categoria_mayor_importe=str(top_value.valor),categoria_mayor_importe_valor=float(top_value.importe_observado_finito),pais_mas_pedidos=str(countries.iloc[0].valor),pais_mas_pedidos_n=int(countries.iloc[0].filas),eventos_anonimos=int(pv('events','user_id','nulos')),sesiones=int(rv('events.session_id y sequence_number','sesiones_no_nulas')),inventario_sold_at_presente=sizes['inventory_items']-int(pv('inventory_items','sold_at','nulos')),inventario_sold_at_ausente=int(pv('inventory_items','sold_at','nulos')),lineas_unidad_sin_sold_at=int(rv(inventory_rel,'lineas_con_unidad_unica_sin_sold_at')),lineas_unidad_comparables=int(rv(inventory_rel,'lineas_con_unidad_unica')),envio_previo_lineas=int(pv('order_items','created_at->shipped_at','secuencia_invertida')),envio_comparable_lineas=int(p.loc[(p.tabla=='order_items')&(p.campo=='created_at->shipped_at')&(p.metrica=='secuencia_invertida'),'denominador'].iloc[0]),pedidos_envio_entrega_horas=float(pv('orders','shipped_at->delivered_at','duracion_media_horas_con_signo')),pedidos_envio_entrega_n=int(p.loc[(p.tabla=='orders')&(p.campo=='shipped_at->delivered_at')&(p.metrica=='duracion_media_horas_con_signo'),'denominador'].iloc[0]),relaciones_comprobadas=len(coverage),relaciones_sin_huerfanos=sum(x['sin_correspondencia']==0 for x in coverage),fecha_min_pedidos=str(pv('orders','created_at','fecha_min_UTC')),fecha_max_pedidos=str(pv('orders','created_at','fecha_max_UTC')))
    (out/'metricas.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
    provenance={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(raw.glob('*.csv'))}
    (out/'fuentes.json').write_text(json.dumps({'origen':'CSV agregados aportados por el usuario tras ejecutar BigQuery; proyecto/dataset y trabajos no confirmados','sha256':provenance},indent=2)+'\n')
    def bar(frame,name,title,xlabel):
        plt.figure(figsize=(9,5));plt.barh(frame.valor.astype(str).iloc[::-1],frame.filas.iloc[::-1]);plt.title(title);plt.xlabel(xlabel);plt.tight_layout();plt.savefig(figures/name,dpi=150);plt.close()
    bar(dist('orders','status'),'estados_pedidos.png','Pedidos por estado registrado','Pedidos')
    bar(cats.head(8),'categorias.png','Categorías con más líneas, todos los estados','Líneas de pedido')
    bar(countries.head(8),'paises.png','País del usuario asociado al pedido','Pedidos')
    bar(dist('events','event_type'),'eventos.png','Eventos por tipo registrado','Eventos')
    monthly.plot.bar(x='valor',y='filas',legend=False,figsize=(14,5));plt.xticks(range(0,len(monthly),12),monthly.valor.iloc[::12],rotation=45);plt.title('Pedidos por mes; extremos de la ventana pueden ser parciales');plt.xlabel('Mes UTC');plt.ylabel('Pedidos');plt.tight_layout();plt.savefig(figures/'pedidos_mensuales.png',dpi=150);plt.close()
    pct=lambda n,den:es(n/den*100,2)
    report=f'''# The Look: informe EDA

## Alcance

Se revisaron tres CSV agregados de BigQuery: **{es(sizes['orders'])} pedidos**, **{es(sizes['order_items'])} líneas**, **{es(sizes['users'])} usuarios**, {es(sizes['products'])} productos, {es(sizes['inventory_items'])} registros de inventario, {es(sizes['events'])} eventos y {es(sizes['distribution_centers'])} centros. Los pedidos abarcan del {m['fecha_min_pedidos'][:10]} al {m['fecha_max_pedidos'][:10]}. El origen exacto, la licencia y los trabajos de consulta no están confirmados en las exportaciones.

## Ventas y demanda observada

Las líneas suman **{es(m['importe_lineas'],2)}**, incluyendo todos los estados; la moneda no está documentada. Solo el estado **Complete** reúne {es(m['pedidos_complete'])} pedidos y {es(m['importe_complete'],2)} de importe de líneas. Ninguno de estos importes confirma cobros o beneficio.

| Estado del pedido | Pedidos | % del total |
| --- | ---: | ---: |
'''+ '\n'.join(f"| {status} | {es(row.filas)} | {pct(row.filas,sizes['orders'])}% |" for status,row in statuses.iterrows())+f'''

Hay **{es(m['lineas_por_pedido'],2)} líneas por pedido** y {es(m['usuarios_con_pedidos'])} usuarios con pedidos. {m['categoria_mas_lineas']} lidera en líneas ({es(m['categoria_mas_lineas_n'])}); {m['categoria_mayor_importe']} lidera en importe ({es(m['categoria_mayor_importe_valor'],2)}). Son registros de demanda en todos los estados, no ventas netas. {m['pais_mas_pedidos']} reúne {pct(m['pais_mas_pedidos_n'],sizes['orders'])}% de los pedidos según el país del usuario, sin confirmar destino de entrega.

![Estados de pedidos](figures/estados_pedidos.png)

## Inventario y logística

**{es(m['inventario_sold_at_ausente'])} unidades carecen de sold_at** y {es(m['inventario_sold_at_presente'])} tienen esa fecha. Sin embargo, las **{es(m['lineas_unidad_sin_sold_at'])} líneas vinculadas a unidades únicas apuntan a registros sin sold_at**. La igualdad entre el total de líneas y unidades con fecha no demuestra que sean las mismas unidades. Esta diferencia debe contrastarse en el origen antes de interpretar disponibilidad o ventas de inventario.

**{es(m['envio_previo_lineas'])} de {es(m['envio_comparable_lineas'])} líneas con ambas fechas ({pct(m['envio_previo_lineas'],m['envio_comparable_lineas'])}%) tienen envío anterior a su creación**. En pedidos, la exportación no señala esa inversión. La duración media envío–entrega es {es(m['pedidos_envio_entrega_horas'],2)} horas para {es(m['pedidos_envio_entrega_n'])} pedidos con ambas fechas; no incluye preparación ni mide cumplimiento de una promesa.

También hay fechas posteriores al inicio de las consultas. No se eliminan: las fechas de líneas y pedidos requieren aclaración antes de comparar tiempos o meses parciales.

## Eventos y relaciones

Se registran **{es(m['sesiones'])} sesiones**. El {pct(m['eventos_anonimos'],sizes['events'])}% de los eventos no tiene user_id. Los tipos product, cart y purchase describen actividad, pero no permiten calcular conversión atribuida a pedidos: no hay un enlace directo de sesión a pedido en el esquema.

Las siete claves candidatas no presentan nulos ni repeticiones. Los nueve enlaces revisados tienen **100% de cobertura entre claves no nulas**, sin padres duplicados. num_of_item coincide con el conteo de líneas de los {es(sizes['orders'])} pedidos comparables; tampoco aparecen diferencias de usuario o producto en las comparaciones exportadas. Un pedido tiene entre una y cuatro líneas: para analizar pedidos hay que agregar esas líneas antes de unir, aunque las claves padre sean únicas.

## Lectura final

La estructura permite relacionar pedidos, usuarios y productos. Los importes dependen del estado y las fechas presentan diferencias relevantes entre pedidos y líneas. **No hay base para afirmar stock disponible, ingresos netos o conversión comercial.** El análisis usa agregados exportados; valida sus balances, sin volver a consultar BigQuery ni auditar sus registros individuales.

Evidencia: [métricas](metricas.json), [relaciones](tables/relaciones.csv), [alertas temporales](tables/alertas_temporales.csv), [categorías](tables/categorias.csv), [países](tables/paises.csv) y [huellas de los CSV](fuentes.json). Gráficos: [categorías](figures/categorias.png), [países](figures/paises.png), [eventos](figures/eventos.png) y [pedidos mensuales](figures/pedidos_mensuales.png).
'''
    (out/'informe_eda.md').write_text(informe('the_look', report),encoding='utf-8')
    print(json.dumps(m,indent=2,ensure_ascii=False))

if __name__=='__main__': main()
