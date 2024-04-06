import DevItem from '../DevItem/DevItem.component';
import './Footer.styles.css';

const Footer = () => {
  const developers_list = [
    {
      student_name: 'Chanpreet Singh',
      image_url: '../../images/chanpreet.jpg',
      roll_no: '2020UCB6038',
      batch: 'B.Tech CSDA',
      semester: '8',
      word_done: 'Frontend UI-UX',
    },
    {
      student_name: 'Aryan Singh',
      image_url: '../../images/aryan.jpg',
      roll_no: '2020UCB6053',
      batch: 'B.Tech CSDA',
      semester: '8',
      word_done: 'API Integeration and model training',
    },
    {
      student_name: 'Himanshu Upreti',
      image_url: '../../images/himanshu.jpg',
      roll_no: '2020UCB6045',
      batch: 'B.Tech CSDA',
      semester: '8',
      word_done: 'backend and API',
    },
  ];
  return (
    <section className="main-footer" id="main-footer">
      <h1>Major Project Team Members</h1>
      <div className="main-footer__items">
        {developers_list.map((item, key) => {
          return <DevItem dev_info={item} key={key} />;
        })}
      </div>
    </section>
  );
};
export default Footer;
