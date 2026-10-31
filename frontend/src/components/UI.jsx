import {AlertCircle,CheckCircle2,LoaderCircle,RefreshCw} from "lucide-react";
export function Header({tag="DATAMARK AI",title,desc,action}){return <div className="pagehead"><div><small className="eyebrow">{tag}</small><h1>{title}</h1><p>{desc}</p></div>{action}</div>}
export function Panel({title,desc,action,children}){return <section className="panel"><div className="panelhead"><div><h3>{title}</h3>{desc&&<p>{desc}</p>}</div>{action}</div>{children}</section>}
export function Stat({label,value,note,icon:Icon,tone="blue"}){return <div className="stat"><div className={`stat-icon ${tone}`}><Icon size={18}/></div><small>{label}</small><b>{value??"—"}</b><p>{note}</p></div>}
export function Loading(){return <div className="loading"><LoaderCircle className="spin"/> Loading data...</div>}
export function ErrorBox({error,retry}){return <div className="error"><AlertCircle/><div><b>Unable to load data</b><p>{error}</p>{retry&&<button className="btn secondary small" onClick={retry}><RefreshCw size={13}/> Retry</button>}</div></div>}
export function Badge({children,tone=""}){return <span className={`badge ${tone}`}>{children}</span>}
export function Empty({title,desc}){return <div className="empty"><CheckCircle2/><b>{title}</b><p>{desc}</p></div>}
