import Head from "next/head";
import Post from "../components/Post";
import { sortByDate } from "../utils";

export default function Home({ posts }) {
  return (
    <>
      <Head>
        <title>Mezi Blog</title>
      </Head>

      <div className="row justify-content-center">
        {posts.map((post, index) => (
          <Post post={post} key={index} />
        ))}
      </div>
    </>
  );
}

export async function getServerSideProps() {
  const response = await fetch("https://meziblog.herokuapp.com/posts");
  const posts = await response.json();
  return {
    props: { posts: posts.sort(sortByDate) },
  };
}
