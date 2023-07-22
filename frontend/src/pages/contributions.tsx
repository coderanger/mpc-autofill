import Head from "next/head";
import React from "react";
import Alert from "react-bootstrap/Alert";

import {
  MakePlayingCards,
  MakePlayingCardsURL,
  ProjectName,
} from "@/common/constants";
import {
  useBackendConfigured,
  useProjectName,
} from "@/features/backend/backendSlice";
import {
  ContributionsPerSource,
  ContributionsSummary,
} from "@/features/contributions/contributions";
import Footer from "@/features/ui/footer";
import { ProjectContainer } from "@/features/ui/layout";
import { NoBackendDefault } from "@/features/ui/noBackendDefault";

function ContributionGuidelines() {
  const projectName = useProjectName();

  return (
    <Alert variant="secondary">
      <h3>Contribution Guidelines</h3>
      <ul>
        <li>
          Image filetype must be either <code>png</code> (recommended) or{" "}
          <code>jpeg</code>
        </li>
        <li>
          When you have multiple versions of a card in the same folder, use
          parentheses to differentiate them &mdash; e.g.{" "}
          <code>Image A.png</code> and <code>Image A (Extended).png</code>
          <ul>
            <li>
              The text in parentheses (e.g. <code>Extended</code> in the above
              example) will be ignored by the search engine.
            </li>
          </ul>
        </li>
        <li>
          If a card has multiple names, use an ampersand to separate them
          &mdash; e.g. <code>Fire & Ice.png</code>
        </li>
        <li>
          Store your token images in a folder called <code>Tokens</code>{" "}
          (anywhere in your repository)
        </li>
        <li>
          Store your cardback images in a folder called <code>Cardbacks</code>{" "}
          (anywhere in your repository)
        </li>
        <li>
          Prepend the names of any folders you don&apos;t want to be indexed by{" "}
          {projectName} with <code>!</code>
          &mdash; e.g. <code>!Misc and Art</code>
        </li>
        <li>
          Limit your files to less than <b>30 MB</b> per image &mdash; this is
          the maximum that Google Scripts can return in one request and the
          maximum that{" "}
          <a href={MakePlayingCardsURL} target="_blank">
            {MakePlayingCards}
          </a>{" "}
          accepts, meaning the desktop client won&apos;t work with images that
          exceed this limit.
        </li>
      </ul>
    </Alert>
  );
}

function ContributionsOrDefault() {
  const backendConfigured = useBackendConfigured();
  return backendConfigured ? (
    <>
      <ContributionsSummary />
      <ContributionGuidelines />
      <ContributionsPerSource />
      <Footer />
    </>
  ) : (
    <NoBackendDefault />
  );
}

export default function Contributions() {
  const projectName = useProjectName();
  return (
    <ProjectContainer>
      <Head>
        <title>{projectName} Contributions</title>
        <meta
          name="description"
          content={`A summary of the image contributors connected to ${ProjectName}.`}
        />
      </Head>
      <ContributionsOrDefault />
    </ProjectContainer>
  );
}
