import "./style/LinkToGalaxyZoo.css";

export default function ExternalLinkButton() {
  const handleClick = () => {
    window.open(
      "https://www.zooniverse.org/projects/zookeeper/galaxy-zoo/",
      "_blank" // abre en nueva pestaña
    );
  };

  return (
    <button className="external-btn" onClick={handleClick}>
      Ir a Galaxy Zoo
    </button>
  );
}
